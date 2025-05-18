//
//  CommunityViewController.m
//  WordMaster
//
//  Created by zq z on 4/27/25.
//
// CommunityViewController.m
#import "CommunityViewController.h"
#import "ExploreViewController.h"
#import "FriendsViewController.h"
#import "CreatePostViewController.h"

@interface CommunityViewController () <UITableViewDelegate, UITableViewDataSource, ExploreViewControllerDelegate,CreatePostDelegate>

@property (nonatomic, strong) UISegmentedControl *segmentedControl;
@property (nonatomic, strong) UIViewController *currentChildController;
@property (nonatomic, strong) UITableView *tableView;

@end

@implementation CommunityViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    self.title = @"社区";
    self.view.backgroundColor = [UIColor systemGroupedBackgroundColor];
    
    self.posts = [NSMutableArray array];
    [self loadPosts];
    
    [self setupNavigationBar];
    [self setupSegmentedControl];
    // 默认显示探索界面
    [self showExploreViewController];
}

- (void)setupSegmentedControl {
    self.segmentedControl = [[UISegmentedControl alloc] initWithItems:@[@"探索", @"好友"]];
    self.segmentedControl.selectedSegmentIndex = 0; // 默认选中探索
    [self.segmentedControl addTarget:self action:@selector(segmentedControlChanged:) forControlEvents:UIControlEventValueChanged];
    self.navigationItem.titleView = self.segmentedControl;
    
    [self showExploreViewController];
}

- (void)segmentedControlChanged:(UISegmentedControl *)sender {
    if (sender.selectedSegmentIndex == 0) {
        [self showExploreViewController];
    } else {
        [self showFriendsViewController];
    }
}

- (void)showExploreViewController {
    if (self.currentChildController) {
        [self.currentChildController.view removeFromSuperview];
        [self.currentChildController removeFromParentViewController];
    }
    
    ExploreViewController *exploreVC = [[ExploreViewController alloc] init];
    exploreVC.posts = self.posts; // 共享数据源
    exploreVC.delegate = self;  // 设置代理为 CommunityViewController
    [self addChildViewController:exploreVC];
    exploreVC.view.frame = self.view.bounds;
    [self.view addSubview:exploreVC.view];
    [exploreVC didMoveToParentViewController:self];
    self.currentChildController = exploreVC;
}

- (void)showFriendsViewController {
    if (self.currentChildController) {
        [self.currentChildController.view removeFromSuperview];
        [self.currentChildController removeFromParentViewController];
    }
    
    FriendsViewController *friendsVC = [[FriendsViewController alloc] init];
    [self addChildViewController:friendsVC];
    friendsVC.view.frame = self.view.bounds;
    [self.view addSubview:friendsVC.view];
    [friendsVC didMoveToParentViewController:self];
    self.currentChildController = friendsVC;
}

#pragma mark - ExploreViewControllerDelegate

- (void)setupNavigationBar {
    // 添加发帖按钮
    UIBarButtonItem *postButton = [[UIBarButtonItem alloc]
        initWithBarButtonSystemItem:UIBarButtonSystemItemAdd
        target:self
        action:@selector(createNewPost)];
    self.navigationItem.rightBarButtonItem = postButton;  // 添加到右上角
    
    // 设置导航栏外观
    if (@available(iOS 13.0, *)) {
        UINavigationBarAppearance *appearance = [[UINavigationBarAppearance alloc] init];
        [appearance configureWithOpaqueBackground];
        appearance.backgroundColor = [UIColor systemBackgroundColor];
        appearance.titleTextAttributes = @{NSForegroundColorAttributeName: [UIColor labelColor]};
        
        self.navigationController.navigationBar.standardAppearance = appearance;
        self.navigationController.navigationBar.scrollEdgeAppearance = appearance;
    }
}

- (void)createNewPost {
    if (self.segmentedControl.selectedSegmentIndex == 0) { // 确保在探索页面
        ExploreViewController *exploreVC = (ExploreViewController *)self.currentChildController;
        CreatePostViewController *createVC = [[CreatePostViewController alloc] init];
        createVC.delegate = exploreVC;
        [self.navigationController pushViewController:createVC animated:YES];
    } else {
        // 处理在好友页面点击发帖的情况
        UIAlertController *alert = [UIAlertController alertControllerWithTitle:@"提示"
                                                        message:@"请在探索页面发布帖子"
                                        preferredStyle:UIAlertControllerStyleAlert];
        [alert addAction:[UIAlertAction actionWithTitle:@"确定" style:UIAlertActionStyleDefault handler:nil]];
        [self presentViewController:alert animated:YES completion:nil];
    }
}

- (void)loadPosts {
    // 从本地加载或初始化默认帖子
    PostModel *p1 = [[PostModel alloc] initWithTitle:@"全球分享" content:@"这是第一个分享的内容" hasAudio:YES avatarName:@"redAvatar" userName:@"Mike" likeCount:100 dislikeCount:10];
        PostModel *p2 = [[PostModel alloc] initWithTitle:@"语言学习"
                                                    content:@"学习一门新语言，提升你的技能"
                                                hasAudio:NO
                                                avatarName:@"blueAvatar"
                                                userName:@"Mark"
                                                likeCount:200
                                            dislikeCount:5];
    
        PostModel *p3 = [[PostModel alloc] initWithTitle:@"旅游推荐"
                                                    content:@"来看看我推荐的旅行地"
                                                hasAudio:YES
                                                avatarName:@"defaultAvatar"
                                                userName:@"Helen"
                                                likeCount:150
                                            dislikeCount:8];
    [self.posts addObjectsFromArray:@[p1, p2, p3]];
}

@end
