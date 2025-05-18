//
//  PostModel.h
//  WordMaster
//
//  Created by zq z on 4/28/25.
//
/// PostModel.h

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

@interface PostModel : NSObject

@property (nonatomic, strong) NSString *title;
@property (nonatomic, strong) NSString *content;
@property (nonatomic, assign) BOOL hasAudio;
@property (nonatomic, strong) NSString *avatarName;
@property (nonatomic, strong) NSString *userName;
@property (nonatomic, assign) NSInteger likeCount;
@property (nonatomic, assign) NSInteger dislikeCount;

// 声明新的初始化方法
- (instancetype)initWithTitle:(NSString *)title
                      content:(NSString *)content
                     hasAudio:(BOOL)hasAudio
                   avatarName:(NSString *)avatarName
                     userName:(NSString *)userName
                    likeCount:(NSInteger)likeCount
                 dislikeCount:(NSInteger)dislikeCount;

@end

NS_ASSUME_NONNULL_END
