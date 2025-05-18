//
//  PostDetailViewController.h
//  WordMaster
//
//  Created by zq z on 4/28/25.
//
#import <UIKit/UIKit.h>
@class PostModel;

@interface PostDetailViewController : UIViewController

@property (nonatomic, strong) PostModel *post;

- (UIColor *)colorForAvatar:(NSString *)avatarName;
- (NSString *)avatarImageNameForAvatar:(NSString *)avatarName;

@end
