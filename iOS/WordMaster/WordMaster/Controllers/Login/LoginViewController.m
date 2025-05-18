//
//  LoginViewController.m
//  WordMaster
//
//  Created by zq z on 4/27/25.
//
#import "LoginViewController.h"
#import "RegisterViewController.h"
#import "UserManager.h"
#import "SceneDelegate.h"
#import "MainTabBarController.h"

@interface LoginViewController ()

@property (nonatomic, strong) UITextField *usernameField;
@property (nonatomic, strong) UITextField *passwordField;

@end

@implementation LoginViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    self.title = @"登录";
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

    UIButton *loginBtn = [UIButton buttonWithType:UIButtonTypeSystem];
    loginBtn.frame = CGRectMake(40, 270, width - 80, 44);
    [loginBtn setTitle:@"登录" forState:UIControlStateNormal];
    [loginBtn addTarget:self action:@selector(handleLogin) forControlEvents:UIControlEventTouchUpInside];
    [self.view addSubview:loginBtn];

    UIButton *registerBtn = [UIButton buttonWithType:UIButtonTypeSystem];
    registerBtn.frame = CGRectMake(40, 330, width - 80, 44);
    [registerBtn setTitle:@"注册" forState:UIControlStateNormal];
    [registerBtn addTarget:self action:@selector(handleRegister) forControlEvents:UIControlEventTouchUpInside];
    [self.view addSubview:registerBtn];
}

- (void)handleLogin {
    NSString *username = self.usernameField.text;
    NSString *password = self.passwordField.text;

    if ([[UserManager sharedManager] loginWithUsername:username password:password]) {
        MainTabBarController *mainTabBarController = [[MainTabBarController alloc] init];
        UIWindowScene *scene = (UIWindowScene *)UIApplication.sharedApplication.connectedScenes.allObjects.firstObject;
        SceneDelegate *sceneDelegate = (SceneDelegate *)scene.delegate;
        sceneDelegate.window.rootViewController = mainTabBarController;
    } else {
        [self showAlert:@"用户名或密码错误"];
    }
}

- (void)handleRegister {
    RegisterViewController *vc = [[RegisterViewController alloc] init];
    [self.navigationController pushViewController:vc animated:YES];
}

- (void)showAlert:(NSString *)message {
    UIAlertController *alert = [UIAlertController alertControllerWithTitle:@"提示"
                                                        message:message
                                        preferredStyle:UIAlertControllerStyleAlert];
    [alert addAction:[UIAlertAction actionWithTitle:@"确定" style:UIAlertActionStyleDefault handler:nil]];
    [self presentViewController:alert animated:YES completion:nil];
}

@end
