//
//  ProfileViewController.m
//  WordMaster
//
//  Created by zq z on 4/27/25.
//
#import "ProfileViewController.h"
#import "UserManager.h"
#import "EditProfileViewController.h"

@interface ProfileViewController () <UITableViewDataSource, UITableViewDelegate, UIImagePickerControllerDelegate, UINavigationControllerDelegate>

@property (nonatomic, strong) UILabel *usernameLabel;
@property (nonatomic, strong) UILabel *progressLabel;
@property (nonatomic, strong) UIImageView *avatarImageView;
@property (nonatomic, strong) UITableView *favoritesTableView;
@property (nonatomic, strong) NSArray<NSString *> *favorites;

// 编辑按钮
@property (nonatomic, strong) UIButton *editAvatarButton;
@property (nonatomic, strong) UIButton *editUsernameButton;
@property (nonatomic, strong) UIButton *editPasswordButton;

@end

@implementation ProfileViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    self.title = @"个人资料";
    self.view.backgroundColor = [UIColor whiteColor];
    
    self.navigationItem.rightBarButtonItem = [[UIBarButtonItem alloc] initWithTitle:@"编辑"
        style:UIBarButtonItemStylePlain
        target:self
        action:@selector(editProfileTapped)];
    
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(editAvatarButtonTapped) name:@"EditAvatar" object:nil];
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(editUsernameButtonTapped) name:@"EditUsername" object:nil];
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(editPasswordButtonTapped) name:@"EditPassword" object:nil];
    
    [self setupUI];
    [self reloadFavorites];
}

- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
    [self reloadFavorites];
}

- (void)setupUI {
    // 用户头像
    self.avatarImageView = [[UIImageView alloc] initWithFrame:CGRectMake(20, 100, 80, 80)];
    self.avatarImageView.contentMode = UIViewContentModeScaleAspectFill;
    self.avatarImageView.layer.cornerRadius = 40;
    self.avatarImageView.clipsToBounds = YES;
    [self.view addSubview:self.avatarImageView];
    
    // 用户名
    self.usernameLabel = [[UILabel alloc] initWithFrame:CGRectMake(120, 130, 200, 30)];
    self.usernameLabel.font = [UIFont boldSystemFontOfSize:22];
    [self.view addSubview:self.usernameLabel];

    // 学习进度
    self.progressLabel = [[UILabel alloc] initWithFrame:CGRectMake(120, 200, 200, 20)];
    self.progressLabel.font = [UIFont systemFontOfSize:16];
    self.progressLabel.textColor = [UIColor darkGrayColor];
    [self.view addSubview:self.progressLabel];
    
    // 收藏列表标题
    UILabel *favoritesTitle = [[UILabel alloc] initWithFrame:CGRectMake(20, 280, 200, 30)];
    favoritesTitle.text = @"收藏的单词";
    favoritesTitle.font = [UIFont boldSystemFontOfSize:18];
    [self.view addSubview:favoritesTitle];

    // 收藏单词表
    self.favoritesTableView = [[UITableView alloc] initWithFrame:CGRectMake(20, 320, self.view.bounds.size.width - 40, self.view.bounds.size.height - 340) style:UITableViewStylePlain];
    self.favoritesTableView.dataSource = self;
    self.favoritesTableView.delegate = self;
    [self.view addSubview:self.favoritesTableView];
}

- (void)editProfileTapped {
    EditProfileViewController *editVC = [[EditProfileViewController alloc] init];
    UINavigationController *nav = [[UINavigationController alloc] initWithRootViewController:editVC];
    nav.modalPresentationStyle = UIModalPresentationFormSheet;
    editVC.didUpdateProfile = ^{
        [self reloadFavorites];
    };
    [self presentViewController:nav animated:YES completion:nil];
}

- (void)reloadFavorites {
    UserModel *user = [[UserManager sharedManager] getCurrentUser];
    self.usernameLabel.text = user.username;
    self.progressLabel.text = [NSString stringWithFormat:@"学习进度：%ld / 50", (long)user.learnedWordsCount];
    
    if (user.avatarName.length > 0) {
        NSString *avatarPath = [self avatarPathForFileName:user.avatarName];
        UIImage *avatar = [UIImage imageWithContentsOfFile:avatarPath];
        self.avatarImageView.image = avatar ?: [self defaultAvatarImage];
    } else {
        self.avatarImageView.image = [self defaultAvatarImage];
    }
    
    self.favorites = [user.collectedWords copy];
    [self.favoritesTableView reloadData];
}

// 返回灰色默认头像图片
- (UIImage *)defaultAvatarImage {
    CGSize size = CGSizeMake(80, 80);
    UIGraphicsBeginImageContextWithOptions(size, NO, 0.0);
    [[UIColor lightGrayColor] setFill];
    UIBezierPath *path = [UIBezierPath bezierPathWithOvalInRect:CGRectMake(0, 0, size.width, size.height)];
    [path fill];
    UIImage *circleImage = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    return circleImage;
}

#pragma mark - 编辑按钮操作

- (void)editAvatarButtonTapped {
    UIImagePickerController *imagePicker = [[UIImagePickerController alloc] init];
    imagePicker.delegate = self;
    imagePicker.sourceType = UIImagePickerControllerSourceTypePhotoLibrary;
    [self presentViewController:imagePicker animated:YES completion:nil];
}

- (void)editUsernameButtonTapped {
    UIAlertController *alertController = [UIAlertController alertControllerWithTitle:@"编辑用户名" message:nil preferredStyle:UIAlertControllerStyleAlert];
    [alertController addTextFieldWithConfigurationHandler:^(UITextField * _Nonnull textField) {
        textField.text = self.usernameLabel.text;
        textField.placeholder = @"请输入新用户名";
    }];
    
    UIAlertAction *saveAction = [UIAlertAction actionWithTitle:@"保存" style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {
        NSString *newUsername = alertController.textFields.firstObject.text;
        if (newUsername.length > 0) {
            UserModel *user = [[UserManager sharedManager] getCurrentUser];
            user.username = newUsername;
            [[UserManager sharedManager] saveUsers];
            [self reloadFavorites];
        }
    }];
    
    [alertController addAction:saveAction];
    [alertController addAction:[UIAlertAction actionWithTitle:@"取消" style:UIAlertActionStyleCancel handler:nil]];
    [self presentViewController:alertController animated:YES completion:nil];
}

- (void)editPasswordButtonTapped {
    UIAlertController *alertController = [UIAlertController alertControllerWithTitle:@"编辑密码" message:nil preferredStyle:UIAlertControllerStyleAlert];
    [alertController addTextFieldWithConfigurationHandler:^(UITextField * _Nonnull textField) {
        textField.placeholder = @"请输入新密码";
        textField.secureTextEntry = YES;
    }];
    
    UIAlertAction *saveAction = [UIAlertAction actionWithTitle:@"保存" style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {
        NSString *newPassword = alertController.textFields.firstObject.text;
        if (newPassword.length > 0) {
            UserModel *user = [[UserManager sharedManager] getCurrentUser];
            user.password = newPassword;
            [[UserManager sharedManager] saveUsers];
        }
    }];
    
    [alertController addAction:saveAction];
    [alertController addAction:[UIAlertAction actionWithTitle:@"取消" style:UIAlertActionStyleCancel handler:nil]];
    [self presentViewController:alertController animated:YES completion:nil];
}

#pragma mark - UIImagePickerControllerDelegate

- (void)imagePickerController:(UIImagePickerController *)picker didFinishPickingMediaWithInfo:(NSDictionary<NSString *,id> *)info {
    UIImage *selectedImage = info[UIImagePickerControllerOriginalImage];
    self.avatarImageView.image = selectedImage;

    // 保存为用户专属头像文件
    NSData *imageData = UIImagePNGRepresentation(selectedImage);
    NSString *avatarFileName = [NSString stringWithFormat:@"avatar_%@.png", [UserManager sharedManager].currentUser.username];
    NSString *avatarPath = [self avatarPathForFileName:avatarFileName];
    [imageData writeToFile:avatarPath atomically:YES];

    // 更新用户模型中的头像文件名
    UserModel *user = [[UserManager sharedManager] getCurrentUser];
    user.avatarName = avatarFileName;
    [[UserManager sharedManager] saveUsers];

    [picker dismissViewControllerAnimated:YES completion:nil];
}

- (NSString *)avatarPathForFileName:(NSString *)fileName {
    NSString *docDir = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES).firstObject;
    return [docDir stringByAppendingPathComponent:fileName];
}
- (void)imagePickerControllerDidCancel:(UIImagePickerController *)picker {
    [picker dismissViewControllerAnimated:YES completion:nil];
}

#pragma mark - UITableViewDataSource

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return self.favorites.count;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    static NSString *cellId = @"FavoriteCell";
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:cellId];
    if (!cell) {
        cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:cellId];
    }
    cell.textLabel.text = self.favorites[indexPath.row];
    return cell;
}

#pragma mark - UITableViewDelegate

- (BOOL)tableView:(UITableView *)tableView canEditRowAtIndexPath:(NSIndexPath *)indexPath {
    return YES;
}

- (void)tableView:(UITableView *)tableView commitEditingStyle:(UITableViewCellEditingStyle)editingStyle
                                               forRowAtIndexPath:(NSIndexPath *)indexPath {
    if (editingStyle == UITableViewCellEditingStyleDelete) {
        NSString *wordToRemove = self.favorites[indexPath.row];
        [[UserManager sharedManager] removeFavoriteWord:wordToRemove];
        [self reloadFavorites];
    }
}

@end
