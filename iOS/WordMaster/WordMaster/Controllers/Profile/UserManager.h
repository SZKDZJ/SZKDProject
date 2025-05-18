//
//  UserManager.h
//  WordMaster
//
//  Created by zq z on 4/29/25.
//
#import <Foundation/Foundation.h>
#import "UserModel.h"

@interface UserManager : NSObject

@property (nonatomic, strong) NSMutableArray<UserModel *> *users;
@property (nonatomic, strong) UserModel *currentUser;

+ (instancetype)sharedManager;
- (void)loadUsers;
- (void)addUser:(UserModel *)user;
- (void)saveUsers;
- (UserModel *)findUserByUsername:(NSString *)username;
- (BOOL)registerUser:(UserModel *)user;
- (BOOL)loginWithUsername:(NSString *)username password:(NSString *)password;

- (BOOL)isWordFavorited:(NSString *)word;
- (void)setFavorite:(BOOL)isFavorite forWord:(NSString *)word;
- (void)removeFavoriteWord:(NSString *)word;
- (UserModel *)getCurrentUser;

@property (nonatomic, strong) NSMutableArray<NSString *> *learnedWords;
@property (nonatomic, assign) NSInteger learnedWordsCount;

@end
