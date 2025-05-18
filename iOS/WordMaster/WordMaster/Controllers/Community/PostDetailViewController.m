//
//  PostDetailViewController.m
//  WordMaster
//
//  Created by zq z on 4/28/25.
//

#import "PostDetailViewController.h"
#import "PostModel.h"

@interface PostDetailViewController ()

@property (nonatomic, strong) UIScrollView *scrollView;
@property (nonatomic, strong) UIView *contentView;
@property (nonatomic, strong) UIImageView *avatarImageView;
@property (nonatomic, strong) UILabel *userNameLabel;
@property (nonatomic, strong) UILabel *postTitleLabel;
@property (nonatomic, strong) UILabel *postContentLabel;
@property (nonatomic, strong) UIButton *playAudioButton;
@property (nonatomic, strong) UIButton *likeButton;
@property (nonatomic, strong) UIButton *dislikeButton;
@property (nonatomic, strong) UIView *separatorLine;

@end

@implementation PostDetailViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    self.view.backgroundColor = [UIColor systemBackgroundColor];
    self.title = @"帖子详情";
    
    [self setupViews];
    [self setupConstraints];
    [self configureWithPost:self.post];
}

- (void)setupViews {
    // 滚动视图
    self.scrollView = [[UIScrollView alloc] init];
    self.scrollView.translatesAutoresizingMaskIntoConstraints = NO;
    [self.view addSubview:self.scrollView];
    
    // 内容视图
    self.contentView = [[UIView alloc] init];
    self.contentView.translatesAutoresizingMaskIntoConstraints = NO;
    [self.scrollView addSubview:self.contentView];
    
    // 头像
    self.avatarImageView = [[UIImageView alloc] init];
    self.avatarImageView.contentMode = UIViewContentModeScaleAspectFill;
    self.avatarImageView.layer.cornerRadius = 20;
    self.avatarImageView.clipsToBounds = YES;
    self.avatarImageView.translatesAutoresizingMaskIntoConstraints = NO;
    [self.contentView addSubview:self.avatarImageView];
    
    // 用户名
    self.userNameLabel = [[UILabel alloc] init];
    self.userNameLabel.font = [UIFont systemFontOfSize:16 weight:UIFontWeightMedium];
    self.userNameLabel.textColor = [UIColor secondaryLabelColor];
    self.userNameLabel.translatesAutoresizingMaskIntoConstraints = NO;
    [self.contentView addSubview:self.userNameLabel];
    
    // 标题
    self.postTitleLabel = [[UILabel alloc] init];
    self.postTitleLabel.font = [UIFont systemFontOfSize:22 weight:UIFontWeightBold];
    self.postTitleLabel.numberOfLines = 0;
    self.postTitleLabel.textColor = [UIColor labelColor];
    self.postTitleLabel.translatesAutoresizingMaskIntoConstraints = NO;
    [self.contentView addSubview:self.postTitleLabel];
    
    // 分隔线
    self.separatorLine = [[UIView alloc] init];
    self.separatorLine.backgroundColor = [UIColor separatorColor];
    self.separatorLine.translatesAutoresizingMaskIntoConstraints = NO;
    [self.contentView addSubview:self.separatorLine];
    
    // 内容
    self.postContentLabel = [[UILabel alloc] init];
    self.postContentLabel.font = [UIFont systemFontOfSize:17];
    self.postContentLabel.textColor = [UIColor labelColor];
    self.postContentLabel.numberOfLines = 0;
    self.postContentLabel.translatesAutoresizingMaskIntoConstraints = NO;
    [self.contentView addSubview:self.postContentLabel];
    
    // 播放按钮
    self.playAudioButton = [UIButton buttonWithType:UIButtonTypeSystem];
    [self.playAudioButton setTitle:@"播放音频" forState:UIControlStateNormal];
    [self.playAudioButton setImage:[UIImage systemImageNamed:@"play.fill"] forState:UIControlStateNormal];
    [self.playAudioButton setTintColor:[UIColor systemGreenColor]];
    self.playAudioButton.titleLabel.font = [UIFont systemFontOfSize:16 weight:UIFontWeightMedium];
    [self.playAudioButton addTarget:self action:@selector(playAudio:) forControlEvents:UIControlEventTouchUpInside];
    self.playAudioButton.translatesAutoresizingMaskIntoConstraints = NO;
    [self.contentView addSubview:self.playAudioButton];
    
    // 点赞按钮
    self.likeButton = [UIButton buttonWithType:UIButtonTypeSystem];
    [self.likeButton setImage:[UIImage systemImageNamed:@"hand.thumbsup"] forState:UIControlStateNormal];
    [self.likeButton setTintColor:[UIColor systemBlueColor]];
    [self.likeButton addTarget:self action:@selector(likePost:) forControlEvents:UIControlEventTouchUpInside];
    self.likeButton.translatesAutoresizingMaskIntoConstraints = NO;
    [self.contentView addSubview:self.likeButton];
    
    // 踩按钮
    self.dislikeButton = [UIButton buttonWithType:UIButtonTypeSystem];
    [self.dislikeButton setImage:[UIImage systemImageNamed:@"hand.thumbsdown"] forState:UIControlStateNormal];
    [self.dislikeButton setTintColor:[UIColor systemRedColor]];
    [self.dislikeButton addTarget:self action:@selector(dislikePost:) forControlEvents:UIControlEventTouchUpInside];
    self.dislikeButton.translatesAutoresizingMaskIntoConstraints = NO;
    [self.contentView addSubview:self.dislikeButton];
}

- (void)setupConstraints {
    CGFloat margin = 16;
    
    [NSLayoutConstraint activateConstraints:@[
        // 滚动视图
        [self.scrollView.topAnchor constraintEqualToAnchor:self.view.safeAreaLayoutGuide.topAnchor],
        [self.scrollView.leadingAnchor constraintEqualToAnchor:self.view.leadingAnchor],
        [self.scrollView.trailingAnchor constraintEqualToAnchor:self.view.trailingAnchor],
        [self.scrollView.bottomAnchor constraintEqualToAnchor:self.view.bottomAnchor],
        
        // 内容视图
        [self.contentView.topAnchor constraintEqualToAnchor:self.scrollView.topAnchor],
        [self.contentView.leadingAnchor constraintEqualToAnchor:self.scrollView.leadingAnchor],
        [self.contentView.trailingAnchor constraintEqualToAnchor:self.scrollView.trailingAnchor],
        [self.contentView.bottomAnchor constraintEqualToAnchor:self.scrollView.bottomAnchor],
        [self.contentView.widthAnchor constraintEqualToAnchor:self.scrollView.widthAnchor],
        
        // 头像
        [self.avatarImageView.topAnchor constraintEqualToAnchor:self.contentView.topAnchor constant:margin],
        [self.avatarImageView.leadingAnchor constraintEqualToAnchor:self.contentView.leadingAnchor constant:margin],
        [self.avatarImageView.widthAnchor constraintEqualToConstant:40],
        [self.avatarImageView.heightAnchor constraintEqualToConstant:40],
        
        // 用户名
        [self.userNameLabel.centerYAnchor constraintEqualToAnchor:self.avatarImageView.centerYAnchor],
        [self.userNameLabel.leadingAnchor constraintEqualToAnchor:self.avatarImageView.trailingAnchor constant:12],
        [self.userNameLabel.trailingAnchor constraintEqualToAnchor:self.contentView.trailingAnchor constant:-margin],
        
        // 标题
        [self.postTitleLabel.topAnchor constraintEqualToAnchor:self.avatarImageView.bottomAnchor constant:20],
        [self.postTitleLabel.leadingAnchor constraintEqualToAnchor:self.contentView.leadingAnchor constant:margin],
        [self.postTitleLabel.trailingAnchor constraintEqualToAnchor:self.contentView.trailingAnchor constant:-margin],
        
        // 分隔线
        [self.separatorLine.topAnchor constraintEqualToAnchor:self.postTitleLabel.bottomAnchor constant:15],
        [self.separatorLine.leadingAnchor constraintEqualToAnchor:self.contentView.leadingAnchor constant:margin],
        [self.separatorLine.trailingAnchor constraintEqualToAnchor:self.contentView.trailingAnchor constant:-margin],
        [self.separatorLine.heightAnchor constraintEqualToConstant:1],
        
        // 内容
        [self.postContentLabel.topAnchor constraintEqualToAnchor:self.separatorLine.bottomAnchor constant:20],
        [self.postContentLabel.leadingAnchor constraintEqualToAnchor:self.contentView.leadingAnchor constant:margin],
        [self.postContentLabel.trailingAnchor constraintEqualToAnchor:self.contentView.trailingAnchor constant:-margin],
        
        // 播放按钮
        [self.playAudioButton.topAnchor constraintEqualToAnchor:self.postContentLabel.bottomAnchor constant:30],
        [self.playAudioButton.centerXAnchor constraintEqualToAnchor:self.contentView.centerXAnchor],
        [self.playAudioButton.heightAnchor constraintEqualToConstant:44],
        
        // 点赞按钮
        [self.likeButton.topAnchor constraintEqualToAnchor:self.playAudioButton.bottomAnchor constant:30],
        [self.likeButton.leadingAnchor constraintEqualToAnchor:self.contentView.leadingAnchor constant:margin * 2],
        [self.likeButton.heightAnchor constraintEqualToConstant:44],
        [self.likeButton.bottomAnchor constraintEqualToAnchor:self.contentView.bottomAnchor constant:-30],
        
        // 踩按钮
        [self.dislikeButton.centerYAnchor constraintEqualToAnchor:self.likeButton.centerYAnchor],
        [self.dislikeButton.trailingAnchor constraintEqualToAnchor:self.contentView.trailingAnchor constant:-margin * 2],
        [self.dislikeButton.heightAnchor constraintEqualToConstant:44]
    ]];
}

#pragma mark - 配置界面内容

- (UIColor *)colorForAvatar:(NSString *)avatarName {
    NSDictionary *colors = @{
        @"defaultAvatar": [UIColor colorWithRed:0.8 green:0.8 blue:0.8 alpha:1],
        @"redAvatar": [UIColor colorWithRed:1.0 green:0.4 blue:0.4 alpha:1],
        @"blueAvatar": [UIColor colorWithRed:0.3 green:0.6 blue:1.0 alpha:1],
        @"greenAvatar": [UIColor colorWithRed:0.4 green:0.7 blue:0.4 alpha:1]
    };
    return colors[avatarName] ?: colors[@"defaultAvatar"];
}

- (void)configureWithPost:(PostModel *)post {
    self.userNameLabel.text = post.userName;
    self.postTitleLabel.text = post.title;
    self.postContentLabel.text = post.content;
    
    // 设置头像背景色（✅ 改成avatarImageView）
    self.avatarImageView.backgroundColor = [self colorForAvatar:post.avatarName];
    
    // 播放按钮显示隐藏
    self.playAudioButton.hidden = !post.hasAudio;
    
    // 点赞数量
    [self.likeButton setTitle:[NSString stringWithFormat:@" %d", post.likeCount] forState:UIControlStateNormal];
    [self.dislikeButton setTitle:[NSString stringWithFormat:@" %d", post.dislikeCount] forState:UIControlStateNormal];
}

#pragma mark - 按钮事件

- (void)playAudio:(UIButton *)sender {
    NSLog(@"播放音频");
    if ([sender.currentTitle isEqualToString:@"播放音频"]) {
        [sender setTitle:@"停止播放" forState:UIControlStateNormal];
        [sender setImage:[UIImage systemImageNamed:@"stop.fill"] forState:UIControlStateNormal];
    } else {
        [sender setTitle:@"播放音频" forState:UIControlStateNormal];
        [sender setImage:[UIImage systemImageNamed:@"play.fill"] forState:UIControlStateNormal];
    }
}

- (void)likePost:(UIButton *)sender {
    self.post.likeCount += 1;
    [self.likeButton setTitle:[NSString stringWithFormat:@" %d", self.post.likeCount] forState:UIControlStateNormal];
    [UIView animateWithDuration:0.2 animations:^{
        sender.transform = CGAffineTransformMakeScale(1.3, 1.3);
    } completion:^(BOOL finished) {
        [UIView animateWithDuration:0.2 animations:^{
            sender.transform = CGAffineTransformIdentity;
        }];
    }];
}

- (void)dislikePost:(UIButton *)sender {
    self.post.dislikeCount += 1;
    [self.dislikeButton setTitle:[NSString stringWithFormat:@" %d", self.post.dislikeCount] forState:UIControlStateNormal];
    [UIView animateWithDuration:0.2 animations:^{
        sender.transform = CGAffineTransformMakeScale(1.3, 1.3);
    } completion:^(BOOL finished) {
        [UIView animateWithDuration:0.2 animations:^{
            sender.transform = CGAffineTransformIdentity;
        }];
    }];
}

@end
