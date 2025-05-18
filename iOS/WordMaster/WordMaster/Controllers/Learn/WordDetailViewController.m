//
//  WordDetailViewController.m
//  WordMaster
//
//  Created by zq z on 4/27/25.
//

#import "WordDetailViewController.h"
#import "WordModel.h"
#import <AVFoundation/AVFoundation.h>
#import "UserManager.h"

@interface WordDetailViewController ()

@property (nonatomic, strong) WordModel *word;
@property (nonatomic, strong) UILabel *wordLabel;
@property (nonatomic, strong) UILabel *pronunciationLabel;
@property (nonatomic, strong) UILabel *definitionLabel;
@property (nonatomic, strong) UIButton *playSoundButton;

@property (nonatomic, strong) AVPlayer *player;
@property (nonatomic, strong) id timeObserver;

@end

@implementation WordDetailViewController

- (instancetype)initWithWord:(WordModel *)word {
    self = [super init];
    if (self) {
        _word = word;
    }
    return self;
}

- (void)viewDidLoad {
    [super viewDidLoad];
    self.title = self.word.word;
    self.view.backgroundColor = [UIColor whiteColor];
    
    [self setupUI];
    [self setupNavigationBar];
}

#pragma mark - UI

- (void)setupUI {
    self.wordLabel = [[UILabel alloc] initWithFrame:CGRectMake(20, 100, self.view.frame.size.width-40, 40)];
    self.wordLabel.text = self.word.word;
    self.wordLabel.font = [UIFont boldSystemFontOfSize:30];
    self.wordLabel.textAlignment = NSTextAlignmentCenter;
    [self.view addSubview:self.wordLabel];
    
    self.pronunciationLabel = [[UILabel alloc] initWithFrame:CGRectMake(20, 150, self.view.frame.size.width-40, 30)];
    self.pronunciationLabel.text = self.word.pronunciation;
    self.pronunciationLabel.font = [UIFont italicSystemFontOfSize:20];
    self.pronunciationLabel.textAlignment = NSTextAlignmentCenter;
    [self.view addSubview:self.pronunciationLabel];
    
    self.definitionLabel = [[UILabel alloc] initWithFrame:CGRectMake(20, 200, self.view.frame.size.width-40, 100)];
    self.definitionLabel.text = self.word.definition;
    self.definitionLabel.font = [UIFont systemFontOfSize:18];
    self.definitionLabel.numberOfLines = 0;
    self.definitionLabel.textAlignment = NSTextAlignmentCenter;
    [self.view addSubview:self.definitionLabel];
    
    self.playSoundButton = [UIButton buttonWithType:UIButtonTypeSystem];
    self.playSoundButton.frame = CGRectMake((self.view.frame.size.width-150)/2, 320, 150, 44);
    [self.playSoundButton setTitle:@"播放发音" forState:UIControlStateNormal];
    [self.playSoundButton addTarget:self action:@selector(playSound) forControlEvents:UIControlEventTouchUpInside];
    self.playSoundButton.layer.cornerRadius = 8;
    self.playSoundButton.backgroundColor = [UIColor systemBlueColor];
    [self.playSoundButton setTitleColor:[UIColor whiteColor] forState:UIControlStateNormal];
    [self.view addSubview:self.playSoundButton];
}

- (void)setupNavigationBar {
    UIBarButtonItem *favoriteButton = [[UIBarButtonItem alloc] initWithTitle:(self.word.isFavorite ? @"已收藏" : @"收藏")
                            style:UIBarButtonItemStylePlain
                                        target:self
                                        action:@selector(toggleFavorite)];
    self.navigationItem.rightBarButtonItem = favoriteButton;
}

#pragma mark - 播放发音

- (void)playSound {
    if (!self.word.audioURL || [self.word.audioURL isEqualToString:@""]) {
        NSLog(@"❌ 没有音频链接");
        return;
    }
    
    [self.playSoundButton setTitle:@"正在播放..." forState:UIControlStateNormal];
    self.playSoundButton.enabled = NO;
    
    [self animateButton:self.playSoundButton];
    
    NSURL *url = [NSURL URLWithString:self.word.audioURL];
    if (!url) {
        NSLog(@"❌ 音频URL无效");
        [self resetPlayButton];
        return;
    }
    
    if (self.player) {
        [self.player pause];
        self.player = nil;
    }
    
    AVPlayerItem *playerItem = [[AVPlayerItem alloc] initWithURL:url];
    self.player = [[AVPlayer alloc] initWithPlayerItem:playerItem];
    [self.player play];
    
    NSLog(@"▶️ 正在播放单词：%@", self.word.word);
    
    __weak typeof(self) weakSelf = self;
    self.timeObserver = [self.player addBoundaryTimeObserverForTimes:@[[NSValue valueWithCMTime:playerItem.duration]]
                                                               queue:dispatch_get_main_queue()
                                                          usingBlock:^{
        [weakSelf resetPlayButton];
    }];
}

- (void)resetPlayButton {
    [self.playSoundButton setTitle:@"播放发音" forState:UIControlStateNormal];
    self.playSoundButton.enabled = YES;
    
    if (self.timeObserver && self.player) {
        [self.player removeTimeObserver:self.timeObserver];
        self.timeObserver = nil;
    }
}

#pragma mark - 收藏

- (void)toggleFavorite {
    self.word.isFavorite = !self.word.isFavorite;
    
    NSString *newTitle = self.word.isFavorite ? @"已收藏" : @"收藏";
    self.navigationItem.rightBarButtonItem.title = newTitle;
    
    [[UserManager sharedManager] setFavorite:self.word.isFavorite forWord:self.word.word];
    
    if ([self.delegate respondsToSelector:@selector(didUpdateFavoriteStatusForWord:)]) {
        [self.delegate didUpdateFavoriteStatusForWord:self.word];
    }
}

#pragma mark - 小动画

- (void)animateButton:(UIButton *)button {
    [UIView animateWithDuration:0.1 animations:^{
        button.transform = CGAffineTransformMakeScale(0.95, 0.95);
    } completion:^(BOOL finished) {
        [UIView animateWithDuration:0.1 animations:^{
            button.transform = CGAffineTransformIdentity;
        }];
    }];
}

@end
