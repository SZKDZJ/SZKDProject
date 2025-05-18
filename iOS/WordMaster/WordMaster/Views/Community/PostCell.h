//
//  PostCell.h
//  WordMaster
//

#import <UIKit/UIKit.h>
#import "PostModel.h"

NS_ASSUME_NONNULL_BEGIN

@interface PostCell : UITableViewCell

- (void)configureWithPost:(PostModel *)post;

@end

NS_ASSUME_NONNULL_END
