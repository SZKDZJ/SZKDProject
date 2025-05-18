//
//  UserModel.m
//  WordMaster
//
//  Created by zq z on 4/29/25.
//

#import "UserModel.h"

@implementation UserModel

- (NSDictionary *)toDictionary {
    return @{
        @"username": self.username ?: @"",
        @"password": self.password ?: @"",
        @"avatarName": self.avatarName ?: @"default_avatar",
        @"collectedWords": self.collectedWords ?: @[],
        @"learnedWords": self.learnedWords ?: @[],
        @"learnedWordsCount": @(self.learnedWordsCount)
    };
}

+ (instancetype)fromDictionary:(NSDictionary *)dict {
    UserModel *user = [[UserModel alloc] init];
    user.username = dict[@"username"];
    user.password = dict[@"password"];
    user.avatarName = dict[@"avatarName"];
    user.collectedWords = [NSMutableArray arrayWithArray:dict[@"collectedWords"]];
    user.learnedWordsCount = [dict[@"learnedWordsCount"] integerValue];
    NSArray *learned = dict[@"learnedWords"];
    if ([learned isKindOfClass:[NSArray class]]) {
        user.learnedWords = [NSMutableArray arrayWithArray:learned];
    } else {
        user.learnedWords = [NSMutableArray array];
    }
    return user;
}

@end
