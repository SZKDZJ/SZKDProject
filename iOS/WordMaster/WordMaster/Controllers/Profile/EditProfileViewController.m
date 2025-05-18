//
//  EditProfileViewController.m
//  WordMaster
//
//  Created by zq z on 4/30/25.
//

// EditProfileViewController.m
#import "EditProfileViewController.h"
#import "UserManager.h"

@interface EditProfileViewController () <UIImagePickerControllerDelegate, UINavigationControllerDelegate>

@property (nonatomic, strong) UIImageView *avatarImageView;
@property (nonatomic, strong) UITextField *usernameField;
@property (nonatomic, strong) UITextField *passwordField;

@end

@implementation EditProfileViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    self.view.backgroundColor = [UIColor systemBackgroundColor];
    self.title = @"编辑资料";

    self.navigationItem.leftBarButtonItem = [[UIBarButtonItem alloc] initWithTitle:@"取消"
                                                                             style:UIBarButtonItemStylePlain
                                                                            target:self
                                                                            action:@selector(dismissSelf)];
    self.navigationItem.rightBarButtonItem = [[UIBarButtonItem alloc] initWithTitle:@"保存"
                                                                              style:UIBarButtonItemStyleDone
                                                                             target:self
                                                                             action:@selector(saveProfile)];

    [self setupUI];
}

- (void)setupUI {
    UserModel *user = [[UserManager sharedManager] getCurrentUser];

    self.avatarImageView = [[UIImageView alloc] initWithFrame:CGRectMake((self.view.bounds.size.width - 100)/2, 100, 100, 100)];
    self.avatarImageView.layer.cornerRadius = 50;
    self.avatarImageView.clipsToBounds = YES;
    self.avatarImageView.userInteractionEnabled = YES;
    self.avatarImageView.contentMode = UIViewContentModeScaleAspectFill;
    [self.view addSubview:self.avatarImageView];

    UITapGestureRecognizer *tap = [[UITapGestureRecognizer alloc] initWithTarget:self action:@selector(changeAvatar)];
    [self.avatarImageView addGestureRecognizer:tap];

    if (user.avatarName.length > 0) {
        NSString *path = [self avatarPathForFileName:user.avatarName];
        self.avatarImageView.image = [UIImage imageWithContentsOfFile:path] ?: [self defaultAvatarImage];
    } else {
        self.avatarImageView.image = [self defaultAvatarImage];
    }

    self.usernameField = [[UITextField alloc] initWithFrame:CGRectMake(40, 230, self.view.bounds.size.width - 80, 40)];
    self.usernameField.placeholder = @"用户名";
    self.usernameField.borderStyle = UITextBorderStyleRoundedRect;
    self.usernameField.text = user.username;
    [self.view addSubview:self.usernameField];

    self.passwordField = [[UITextField alloc] initWithFrame:CGRectMake(40, 290, self.view.bounds.size.width - 80, 40)];
    self.passwordField.placeholder = @"新密码";
    self.passwordField.secureTextEntry = YES;
    self.passwordField.borderStyle = UITextBorderStyleRoundedRect;
    [self.view addSubview:self.passwordField];
}

- (UIImage *)defaultAvatarImage {
    CGSize size = CGSizeMake(100, 100);
    UIGraphicsBeginImageContextWithOptions(size, NO, 0.0);
    [[UIColor lightGrayColor] setFill];
    UIBezierPath *path = [UIBezierPath bezierPathWithOvalInRect:CGRectMake(0, 0, size.width, size.height)];
    [path fill];
    UIImage *image = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    return image;
}

- (NSString *)avatarPathForFileName:(NSString *)fileName {
    NSString *docDir = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES).firstObject;
    return [docDir stringByAppendingPathComponent:fileName];
}

- (void)changeAvatar {
    UIImagePickerController *picker = [[UIImagePickerController alloc] init];
    picker.delegate = self;
    picker.sourceType = UIImagePickerControllerSourceTypePhotoLibrary;
    [self presentViewController:picker animated:YES completion:nil];
}

- (void)imagePickerController:(UIImagePickerController *)picker didFinishPickingMediaWithInfo:(NSDictionary<NSString *,id> *)info {
    UIImage *image = info[UIImagePickerControllerOriginalImage];
    self.avatarImageView.image = image;
    [picker dismissViewControllerAnimated:YES completion:nil];
}

- (void)saveProfile {
    UserModel *user = [[UserManager sharedManager] getCurrentUser];

    // 保存头像
    UIImage *avatar = self.avatarImageView.image;
    NSData *data = UIImagePNGRepresentation(avatar);
    NSString *fileName = [NSString stringWithFormat:@"avatar_%@.png", user.username];
    NSString *path = [self avatarPathForFileName:fileName];
    [data writeToFile:path atomically:YES];
    user.avatarName = fileName;

    // 用户名
    if (self.usernameField.text.length > 0) {
        user.username = self.usernameField.text;
    }

    // 密码
    if (self.passwordField.text.length > 0) {
        user.password = self.passwordField.text;
    }

    [[UserManager sharedManager] saveUsers];
    
    if (self.didUpdateProfile) {
        self.didUpdateProfile();
    }

    [self dismissViewControllerAnimated:YES completion:nil];
}

- (void)dismissSelf {
    [self dismissViewControllerAnimated:YES completion:nil];
}

@end
