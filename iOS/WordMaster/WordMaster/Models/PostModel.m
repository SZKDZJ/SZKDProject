//
//  PostModel.m
//  WordMaster
//
//  Created by zq z on 4/28/25.
//
// PostModel.m

#import "PostModel.h"

@implementation PostModel

- (instancetype)initWithTitle:(NSString *)title
                      content:(NSString *)content
                     hasAudio:(BOOL)hasAudio
                   avatarName:(NSString *)avatarName
                     userName:(NSString *)userName
                    likeCount:(NSInteger)likeCount
                 dislikeCount:(NSInteger)dislikeCount {
    self = [super init];
    if (self) {
        _title = title;
        _content = content;
        _hasAudio = hasAudio;
        _avatarName = avatarName;
        _userName = userName;
        _likeCount = likeCount;
        _dislikeCount = dislikeCount;
    }
    return self;
}

@end
