//
//  EditProfileViewController.h
//  WordMaster
//
//  Created by zq z on 4/30/25.
//
#import <UIKit/UIKit.h>

@interface EditProfileViewController : UIViewController

@property (nonatomic, copy) void (^didUpdateProfile)(void); // 回调，用于更新主页面显示

@end
