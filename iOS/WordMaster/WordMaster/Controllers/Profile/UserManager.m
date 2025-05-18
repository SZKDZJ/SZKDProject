//
//  UserManager.m
//  WordMaster
//
//  Created by zq z on 4/29/25.
//
#import "UserManager.h"

@implementation UserManager

+ (instancetype)sharedManager {
    static UserManager *manager;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        manager = [[UserManager alloc] init];
        [manager loadUsers];
    });
    return manager;
}

- (NSString *)dataFilePath {
    NSString *path = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES).firstObject;
    return [path stringByAppendingPathComponent:@"userData.json"];
}

- (void)loadUsers {
    self.users = [NSMutableArray array];
    
    NSString *filePath = [self dataFilePath];
    NSData *data = [NSData dataWithContentsOfFile:filePath];
    if (!data) {
        NSString *defaultPath = [[NSBundle mainBundle] pathForResource:@"userData" ofType:@"json"];
        data = [NSData dataWithContentsOfFile:defaultPath];
    }

    if (data) {
        NSArray *array = [NSJSONSerialization JSONObjectWithData:data options:kNilOptions error:nil];
        for (NSDictionary *dict in array) {
            UserModel *user = [UserModel fromDictionary:dict];

            // 防御性初始化，兼容老数据
            if (!user.learnedWords) {
                user.learnedWords = [NSMutableArray array];
            }
            user.learnedWordsCount = user.learnedWords.count;

            [self.users addObject:user];
        }
    }
}

- (void)saveUsers {
    NSMutableArray *dataArray = [NSMutableArray array];
    for (UserModel *user in self.users) {
        [dataArray addObject:[user toDictionary]];
    }
    NSData *data = [NSJSONSerialization dataWithJSONObject:dataArray options:NSJSONWritingPrettyPrinted error:nil];
    [data writeToFile:[self dataFilePath] atomically:YES];
}

- (UserModel *)findUserByUsername:(NSString *)username {
    for (UserModel *user in self.users) {
        if ([user.username isEqualToString:username]) {
            return user;
        }
    }
    return nil;
}

- (BOOL)registerUser:(UserModel *)newUser {
    for (UserModel *user in self.users) {
        if ([user.username isEqualToString:newUser.username]) {
            return NO; // 用户名已存在
        }
    }
    [self.users addObject:newUser];
    [self saveUsers];
    return YES;
}

- (BOOL)loginWithUsername:(NSString *)username password:(NSString *)password {
    UserModel *user = [self findUserByUsername:username];
    if (user && [user.password isEqualToString:password]) {
        self.currentUser = user;
        return YES;
    }
    return NO;
}

- (BOOL)isWordFavorited:(NSString *)word {
    return [self.currentUser.collectedWords containsObject:word];
}

- (void)setFavorite:(BOOL)isFavorite forWord:(NSString *)word {
    if (isFavorite && ![self.currentUser.collectedWords containsObject:word]) {
        [self.currentUser.collectedWords addObject:word];
    } else if (!isFavorite && [self.currentUser.collectedWords containsObject:word]) {
        [self.currentUser.collectedWords removeObject:word];
    }
    [self saveUsers];
}

- (void)removeFavoriteWord:(NSString *)word {
    [self.currentUser.collectedWords removeObject:word];
    [self saveUsers];
}

- (UserModel *)getCurrentUser {
    return self.currentUser;
}

- (void)addUser:(UserModel *)user {
    [self.users addObject:user];
}



@end
