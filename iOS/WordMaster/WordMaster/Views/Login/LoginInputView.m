//
//  LoginInputView.m
//  WordMaster
//
//  Created by zq z on 4/27/25.
//

#import "LoginInputView.h"

@implementation LoginInputView

- (instancetype)init {
    self = [super init];
    if (self) {
        self.usernameField = [[UITextField alloc] init];
        self.usernameField.placeholder = @"用户名";
        self.usernameField.borderStyle = UITextBorderStyleRoundedRect;
        [self addSubview:self.usernameField];
        
        self.passwordField = [[UITextField alloc] init];
        self.passwordField.placeholder = @"密码";
        self.passwordField.secureTextEntry = YES;
        self.passwordField.borderStyle = UITextBorderStyleRoundedRect;
        [self addSubview:self.passwordField];
    }
    return self;
}

- (void)layoutSubviews {
    [super layoutSubviews];
    
    self.usernameField.frame = CGRectMake(0, 0, self.bounds.size.width, 44);
    self.passwordField.frame = CGRectMake(0, 60, self.bounds.size.width, 44);
}

@end
