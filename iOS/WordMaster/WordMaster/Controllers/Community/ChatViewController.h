//
//  ChatViewController.h
//  WordMaster
//
//  Created by zq z on 4/28/25.
//
#import <UIKit/UIKit.h>

@interface ChatViewController : UIViewController <UITableViewDelegate, UITableViewDataSource, UITextFieldDelegate>

@property (nonatomic, strong) NSString *friendName;
@property (nonatomic, strong) NSMutableArray *messages;
@property (nonatomic, strong) UITableView *tableView;
@property (nonatomic, strong) UITextField *messageField;
@property (nonatomic, strong) UIButton *sendButton;

@end


