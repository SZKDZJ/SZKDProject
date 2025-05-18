//
//  WordDetailViewController.h
//  WordMaster
//
//  Created by zq z on 4/27/25.
//

#import <UIKit/UIKit.h>
@class WordModel;

@protocol WordDetailViewControllerDelegate <NSObject>
- (void)didUpdateFavoriteStatusForWord:(WordModel *)word;
@end

@interface WordDetailViewController : UIViewController

- (instancetype)initWithWord:(WordModel *)word;
@property (nonatomic, weak) id<WordDetailViewControllerDelegate> delegate;

@end
