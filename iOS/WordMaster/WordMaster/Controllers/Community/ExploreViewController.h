//  ExploreViewController.h
//  WordMaster
//
//  Created by zq z on 4/28/25.
//

#import <UIKit/UIKit.h>
#import "CreatePostViewController.h"

NS_ASSUME_NONNULL_BEGIN

// 创建代理协议
@protocol ExploreViewControllerDelegate <NSObject>
- (void)didCreateNewPost:(PostModel *)post;
@end

@interface ExploreViewController : UIViewController <UITableViewDelegate, UITableViewDataSource, CreatePostDelegate>

@property (nonatomic, weak) id<ExploreViewControllerDelegate> delegate;
@property (nonatomic, strong) NSMutableArray<PostModel *> *posts;
@end

NS_ASSUME_NONNULL_END
