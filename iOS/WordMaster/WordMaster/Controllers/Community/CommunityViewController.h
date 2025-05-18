//
//  CommunityViewController.h
//  WordMaster
//
//  Created by zq z on 4/27/25.
//

#import <UIKit/UIKit.h>
#import "PostModel.h"

NS_ASSUME_NONNULL_BEGIN

@interface CommunityViewController : UIViewController
@property (nonatomic, strong) NSMutableArray<PostModel *> *posts;
@end

NS_ASSUME_NONNULL_END
