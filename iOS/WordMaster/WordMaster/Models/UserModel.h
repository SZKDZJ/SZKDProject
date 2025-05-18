//
//  UserModel.h
//  WordMaster
//
//  Created by zq z on 4/29/25.
//

// UserModel.h
#import <Foundation/Foundation.h>

@interface UserModel : NSObject

@property (nonatomic, strong) NSString *username;
@property (nonatomic, strong) NSString *password;
@property (nonatomic, strong) NSString *avatarName; // 头像名
@property (nonatomic, strong) NSMutableArray<NSString *> *collectedWords;
@property (nonatomic, assign) NSInteger learnedWordsCount;
@property (nonatomic, strong) NSMutableArray<NSString *> *learnedWords;

- (NSDictionary *)toDictionary;
+ (instancetype)fromDictionary:(NSDictionary *)dict;

@end
