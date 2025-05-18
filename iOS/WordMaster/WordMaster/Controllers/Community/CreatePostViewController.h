//
//  CreatePostViewController.h
//  WordMaster
//
//  Created by zq z on 4/28/25.
//
#import <UIKit/UIKit.h> 
#import "PostModel.h"

@class CreatePostViewController;

@protocol CreatePostDelegate <NSObject>
- (void)didCreateNewPost:(PostModel *)post;
@end

@interface CreatePostViewController : UIViewController

@property (nonatomic, weak) id<CreatePostDelegate> delegate;
@property (nonatomic, copy) NSString *currentUserName;
@property (nonatomic, copy) NSString *currentAvatarName;

@end
