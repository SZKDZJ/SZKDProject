//
//  RegisterViewController.m
//  WordMaster
//
//  Created by zq z on 4/27/25.
//
#import "RegisterViewController.h"
#import "UserManager.h"
#import "UserModel.h"

@interface RegisterViewController ()

@property (nonatomic, strong) UITextField *usernameField;
@property (nonatomic, strong) UITextField *passwordField;

@end

@implementation RegisterViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    self.title = @"注册";
    self.view.backgroundColor = [UIColor whiteColor];

    CGFloat width = self.view.frame.size.width;

    _usernameField = [[UITextField alloc] initWithFrame:CGRectMake(40, 150, width - 80, 40)];
    _usernameField.placeholder = @"用户名";
    _usernameField.borderStyle = UITextBorderStyleRoundedRect;
    [self.view addSubview:_usernameField];

    _passwordField = [[UITextField alloc] initWithFrame:CGRectMake(40, 210, width - 80, 40)];
    _passwordField.placeholder = @"密码";
    _passwordField.secureTextEntry = YES;
    _passwordField.borderStyle = UITextBorderStyleRoundedRect;
    [self.view addSubview:_passwordField];

    UIButton *registerBtn = [UIButton buttonWithType:UIButtonTypeSystem];
    registerBtn.frame = CGRectMake(40, 270, width - 80, 44);
    [registerBtn setTitle:@"注册" forState:UIControlStateNormal];
    [registerBtn addTarget:self action:@selector(handleRegister) forControlEvents:UIControlEventTouchUpInside];
    [self.view addSubview:registerBtn];
}

- (void)handleRegister {
    NSString *username = self.usernameField.text;
    NSString *password = self.passwordField.text;

    if (username.length == 0 || password.length == 0) {
        [self showAlert:@"请输入用户名和密码"];
        return;
    }

    UserModel *newUser = [[UserModel alloc] init];
    newUser.username = username;
    newUser.password = password;
    newUser.avatarName = @"#CCCCCC";
    newUser.collectedWords = [NSMutableArray array];
    newUser.learnedWordsCount = 0;
    
    if ([[UserManager sharedManager] registerUser:newUser]) {
        [self.navigationController popViewControllerAnimated:YES];
    } else {
        [self showAlert:@"用户名已存在"];
    }
}

- (void)showAlert:(NSString *)message {
    UIAlertController *alert = [UIAlertController alertControllerWithTitle:@"提示"
                                                                   message:message
                                                            preferredStyle:UIAlertControllerStyleAlert];
    [alert addAction:[UIAlertAction actionWithTitle:@"确定" style:UIAlertActionStyleDefault handler:nil]];
    [self presentViewController:alert animated:YES completion:nil];
}

@end
