//
//  PostCell.m
//  WordMaster
//

#import "PostCell.h"

@interface PostCell ()

@property (nonatomic, strong) UIView *avatarView;
@property (nonatomic, strong) UILabel *userNameLabel;
@property (nonatomic, strong) UILabel *titleLabel;
@property (nonatomic, strong) UILabel *contentLabel;
@property (nonatomic, strong) UIImageView *audioIcon;

@end

@implementation PostCell

- (instancetype)initWithStyle:(UITableViewCellStyle)style reuseIdentifier:(NSString *)reuseIdentifier {
    self = [super initWithStyle:style reuseIdentifier:reuseIdentifier];
    if (self) {
        [self setupSubviews];
        [self setupConstraints];
    }
    return self;
}

- (void)setupSubviews {
    // 头像
    self.avatarView = [[UIView alloc] init];
    self.avatarView.layer.cornerRadius = 20;
    self.avatarView.clipsToBounds = YES;
    [self.contentView addSubview:self.avatarView];
    
    // 用户名
    self.userNameLabel = [[UILabel alloc] init];
    self.userNameLabel.font = [UIFont systemFontOfSize:14 weight:UIFontWeightMedium];
    self.userNameLabel.textColor = [UIColor secondaryLabelColor];
    [self.contentView addSubview:self.userNameLabel];
    
    // 标题
    self.titleLabel = [[UILabel alloc] init];
    self.titleLabel.font = [UIFont systemFontOfSize:18 weight:UIFontWeightSemibold];
    self.titleLabel.textColor = [UIColor labelColor];
    self.titleLabel.numberOfLines = 0;
    [self.contentView addSubview:self.titleLabel];
    
    // 内容
    self.contentLabel = [[UILabel alloc] init];
    self.contentLabel.font = [UIFont systemFontOfSize:15];
    self.contentLabel.textColor = [UIColor secondaryLabelColor];
    self.contentLabel.numberOfLines = 2;
    [self.contentView addSubview:self.contentLabel];
    
    // 音频图标
    self.audioIcon = [[UIImageView alloc] init];
    self.audioIcon.image = [UIImage systemImageNamed:@"speaker.wave.2.fill"];
    self.audioIcon.tintColor = [UIColor systemBlueColor];
    self.audioIcon.contentMode = UIViewContentModeScaleAspectFit;
    [self.contentView addSubview:self.audioIcon];
    
    // 背景视图
    UIView *bgView = [[UIView alloc] init];
    bgView.backgroundColor = [UIColor secondarySystemBackgroundColor];
    bgView.layer.cornerRadius = 12;
    self.backgroundView = bgView;
    
    // 选中状态
    self.selectionStyle = UITableViewCellSelectionStyleNone;
}

- (void)setupConstraints {
    CGFloat margin = 16;
    
    self.avatarView.translatesAutoresizingMaskIntoConstraints = NO;
    self.userNameLabel.translatesAutoresizingMaskIntoConstraints = NO;
    self.titleLabel.translatesAutoresizingMaskIntoConstraints = NO;
    self.contentLabel.translatesAutoresizingMaskIntoConstraints = NO;
    self.audioIcon.translatesAutoresizingMaskIntoConstraints = NO;
    
    [NSLayoutConstraint activateConstraints:@[
        // 头像
        [self.avatarView.leadingAnchor constraintEqualToAnchor:self.contentView.leadingAnchor constant:margin],
        [self.avatarView.topAnchor constraintEqualToAnchor:self.contentView.topAnchor constant:margin],
        [self.avatarView.widthAnchor constraintEqualToConstant:40],
        [self.avatarView.heightAnchor constraintEqualToConstant:40],
        
        // 用户名
        [self.userNameLabel.leadingAnchor constraintEqualToAnchor:self.avatarView.trailingAnchor constant:12],
        [self.userNameLabel.topAnchor constraintEqualToAnchor:self.avatarView.topAnchor],
        [self.userNameLabel.trailingAnchor constraintEqualToAnchor:self.contentView.trailingAnchor constant:-margin],
        
        // 标题
        [self.titleLabel.leadingAnchor constraintEqualToAnchor:self.userNameLabel.leadingAnchor],
        [self.titleLabel.topAnchor constraintEqualToAnchor:self.userNameLabel.bottomAnchor constant:6],
        [self.titleLabel.trailingAnchor constraintEqualToAnchor:self.contentView.trailingAnchor constant:-margin],
        
        // 内容
        [self.contentLabel.leadingAnchor constraintEqualToAnchor:self.titleLabel.leadingAnchor],
        [self.contentLabel.topAnchor constraintEqualToAnchor:self.titleLabel.bottomAnchor constant:8],
        [self.contentLabel.trailingAnchor constraintEqualToAnchor:self.titleLabel.trailingAnchor],
        [self.contentLabel.bottomAnchor constraintEqualToAnchor:self.contentView.bottomAnchor constant:-margin],
        
        // 音频图标
        [self.audioIcon.trailingAnchor constraintEqualToAnchor:self.contentView.trailingAnchor constant:-margin],
        [self.audioIcon.centerYAnchor constraintEqualToAnchor:self.userNameLabel.centerYAnchor],
        [self.audioIcon.widthAnchor constraintEqualToConstant:20],
        [self.audioIcon.heightAnchor constraintEqualToConstant:20]
    ]];
}

- (void)configureWithPost:(PostModel *)post {
    // 确保 avatarView 的背景色设置正确
    self.avatarView.backgroundColor = [self colorForAvatar:post.avatarName];
    self.userNameLabel.text = post.userName;
    // 调试输出颜色值
    NSLog(@"设置头像颜色: %@, 颜色值: %@", post.avatarName, [self colorForAvatar:post.avatarName]);
    
    // 确保 avatarView 可见
    self.avatarView.hidden = NO;
    self.avatarView.alpha = 1.0;
    
    // 移除可能存在的子视图
    for (UIView *subview in self.avatarView.subviews) {
        [subview removeFromSuperview];
    }
    
    // 其他配置保持不变
    self.userNameLabel.text = post.userName;
    self.titleLabel.text = post.title;
    self.contentLabel.text = post.content;
    self.audioIcon.hidden = !post.hasAudio;
}

- (UIColor *)colorForAvatar:(NSString *)avatarName {
    NSDictionary *colors = @{
        @"defaultAvatar": [UIColor colorWithRed:0.8 green:0.8 blue:0.8 alpha:1],  // 浅灰色
        @"redAvatar": [UIColor colorWithRed:1.0 green:0.4 blue:0.4 alpha:1],     // 红色
        @"blueAvatar": [UIColor colorWithRed:0.3 green:0.6 blue:1.0 alpha:1],    // 蓝色
        @"greenAvatar": [UIColor colorWithRed:0.4 green:0.7 blue:0.4 alpha:1]    // 绿色
    };
    UIColor *color = colors[avatarName] ?: colors[@"defaultAvatar"];
    
    // 调试输出
    NSLog(@"头像名称: %@, 返回颜色: %@", avatarName, color);
    
    return color;
}

@end
