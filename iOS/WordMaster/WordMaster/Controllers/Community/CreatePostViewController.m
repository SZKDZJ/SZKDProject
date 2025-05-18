//
//  CreatePostViewController.m
//  WordMaster
//
//  Created by zq z on 4/28/25.
//
// CreatePostViewController.m
#import "CreatePostViewController.h"
#import "PostModel.h"

@interface CreatePostViewController () <UITextViewDelegate>

@property (nonatomic, strong) UITextField *titleField;
@property (nonatomic, strong) UITextView *contentTextView;
@property (nonatomic, strong) UILabel *placeholderLabel;
@property (nonatomic, strong) UISwitch *audioSwitch;

@end

@implementation CreatePostViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    self.title = @"发布帖子";
    self.view.backgroundColor = [UIColor systemBackgroundColor];
    
    [self setupViews];
    [self setupNavigationBar];
    [self setupGestureRecognizer];
}

- (void)setupViews {
    CGFloat margin = 16;
    CGFloat width = self.view.bounds.size.width - 2 * margin;
    
    // 标题输入框
    self.titleField = [[UITextField alloc] initWithFrame:CGRectMake(margin, 100, width, 44)];
    self.titleField.placeholder = @"请输入标题（最多30个字）";
    self.titleField.borderStyle = UITextBorderStyleRoundedRect;
    self.titleField.font = [UIFont systemFontOfSize:16];
    self.titleField.returnKeyType = UIReturnKeyNext;
    self.titleField.delegate = self;
    
    // 内容输入框
    self.contentTextView = [[UITextView alloc] initWithFrame:CGRectMake(margin, 160, width, 200)];
    self.contentTextView.font = [UIFont systemFontOfSize:16];
    self.contentTextView.layer.borderWidth = 0.5;
    self.contentTextView.layer.borderColor = [UIColor separatorColor].CGColor;
    self.contentTextView.layer.cornerRadius = 8;
    self.contentTextView.delegate = self;
    
    // 占位文字
    self.placeholderLabel = [[UILabel alloc] initWithFrame:CGRectMake(5, 8, width - 10, 20)];
    self.placeholderLabel.text = @"分享你的想法...";
    self.placeholderLabel.textColor = [UIColor placeholderTextColor];
    self.placeholderLabel.font = [UIFont systemFontOfSize:16];
    [self.contentTextView addSubview:self.placeholderLabel];
    
    // 音频开关
    UILabel *audioLabel = [[UILabel alloc] initWithFrame:CGRectMake(margin, 380, 100, 30)];
    audioLabel.text = @"添加音频";
    audioLabel.font = [UIFont systemFontOfSize:14];
    
    self.audioSwitch = [[UISwitch alloc] initWithFrame:CGRectMake(width - 60, 375, 0, 0)];
    self.audioSwitch.on = NO;
    
    [self.view addSubview:self.titleField];
    [self.view addSubview:self.contentTextView];
    [self.view addSubview:audioLabel];
    [self.view addSubview:self.audioSwitch];
}

- (void)setupNavigationBar {
    UIBarButtonItem *postButton = [[UIBarButtonItem alloc] initWithTitle:@"发布"
                                                        style:UIBarButtonItemStyleDone
                                                        target:self
                                                        action:@selector(post)];
    self.navigationItem.rightBarButtonItem = postButton;
}

- (void)setupGestureRecognizer {
    UITapGestureRecognizer *tap = [[UITapGestureRecognizer alloc] initWithTarget:self action:@selector(dismissKeyboard)];
    [self.view addGestureRecognizer:tap];
}

- (void)dismissKeyboard {
    [self.view endEditing:YES];
}

#pragma mark - UITextViewDelegate

- (void)textViewDidChange:(UITextView *)textView {
    self.placeholderLabel.hidden = textView.text.length > 0;
}

#pragma mark - Post Action

// CreatePostViewController.m
- (void)post {
    NSString *title = self.titleField.text;
    NSString *content = self.contentTextView.text;
    
    if (title.length == 0 || content.length == 0) {
        UIAlertController *alert = [UIAlertController alertControllerWithTitle:@"提示"
                                                        message:@"标题和内容不能为空"
                                        preferredStyle:UIAlertControllerStyleAlert];
        [alert addAction:[UIAlertAction actionWithTitle:@"确定" style:UIAlertActionStyleDefault handler:nil]];
        
        PostModel *newPost = [[PostModel alloc] initWithTitle:title
                                                       content:content
                                                      hasAudio:self.audioSwitch.isOn
                                                    avatarName:self.currentAvatarName ?: @"defaultAvatar"
                                                      userName:self.currentUserName ?: @"当前用户"
                                                     likeCount:0
                                                  dislikeCount:0];
        
        [self presentViewController:alert animated:YES completion:nil];
        return;
    }
    
    // 创建新帖子
    PostModel *newPost = [[PostModel alloc] initWithTitle:title
                                               content:content
                                              hasAudio:self.audioSwitch.isOn
                                             avatarName:@"defaultAvatar"
                                               userName:@"当前用户"
                                                likeCount:0
                                             dislikeCount:0];
    
    // 通过代理回调
    if ([self.delegate respondsToSelector:@selector(didCreateNewPost:)]) {
        [self.delegate didCreateNewPost:newPost];
    }
    
    [self.navigationController popViewControllerAnimated:YES];
}

@end
