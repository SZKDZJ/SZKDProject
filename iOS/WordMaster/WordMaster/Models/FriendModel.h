//
//  FriendModel.h
//  WordMaster
//
//  Created by zq z on 4/28/25.
//
#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

@interface FriendModel : NSObject

@property (nonatomic, strong) NSString *name;
@property (nonatomic, strong) NSString *status;

- (instancetype)initWithName:(NSString *)name status:(NSString *)status;

@end

NS_ASSUME_NONNULL_END
