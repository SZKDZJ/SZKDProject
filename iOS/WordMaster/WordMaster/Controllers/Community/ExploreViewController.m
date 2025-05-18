//  ExploreViewController.m
//  WordMaster
//
//  Created by zq z on 4/28/25.
//

#import "ExploreViewController.h"
#import "PostCell.h"
#import "PostModel.h"
#import "PostDetailViewController.h"
#import "CreatePostViewController.h"

@interface ExploreViewController () <CreatePostDelegate, UITableViewDelegate, UITableViewDataSource>

@property (nonatomic, strong) UITableView *tableView;
@property (nonatomic, strong) UIRefreshControl *refreshControl;

@end

@implementation ExploreViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    self.title = @"探索";
    self.view.backgroundColor = [UIColor systemBackgroundColor];
    
    //[self setupPosts];
    [self setupTableView];
    [self setupRefreshControl];
}

- (void)setupNavigationBar {
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

- (void)setupRefreshControl {
    self.refreshControl = [[UIRefreshControl alloc] init];
    [self.refreshControl addTarget:self action:@selector(refreshPosts) forControlEvents:UIControlEventValueChanged];
    if (@available(iOS 10.0, *)) {
        self.tableView.refreshControl = self.refreshControl;
    } else {
        [self.tableView addSubview:self.refreshControl];
    }
}

- (void)refreshPosts {
    // 模拟网络请求延迟
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(1.5 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        [self.refreshControl endRefreshing];
        // 这里可以添加实际的数据刷新逻辑
    });
}

- (void)createNewPost {
    CreatePostViewController *createVC = [[CreatePostViewController alloc] init];
    createVC.delegate = self;
    [self.navigationController pushViewController:createVC animated:YES];
}

//- (void)setupPosts {
//    // 示例数据
//    PostModel *p1 = [[PostModel alloc] initWithTitle:@"全球分享"
//                                                content:@"这是第一个分享的内容"
//                                            hasAudio:YES
//                                            avatarName:@"redAvatar"
//                                            userName:@"Mike"
//                                            likeCount:100
//                                        dislikeCount:10];
//    
//    PostModel *p2 = [[PostModel alloc] initWithTitle:@"语言学习"
//                                                content:@"学习一门新语言，提升你的技能"
//                                            hasAudio:NO
//                                            avatarName:@"blueAvatar"
//                                            userName:@"Mark"
//                                            likeCount:200
//                                        dislikeCount:5];
//    
//    PostModel *p3 = [[PostModel alloc] initWithTitle:@"旅游推荐"
//                                                content:@"来看看我推荐的旅行地"
//                                            hasAudio:YES
//                                            avatarName:@"defaultAvatar"
//                                            userName:@"Helen"
//                                            likeCount:150
//                                        dislikeCount:8];
//    
//    // 使用 NSMutableArray
//    self.posts = [NSMutableArray arrayWithObjects:p1, p2, p3, nil];
//}

- (void)setupTableView {
    self.tableView = [[UITableView alloc] initWithFrame:self.view.bounds style:UITableViewStylePlain];
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    self.tableView.separatorStyle = UITableViewCellSeparatorStyleNone;
    self.tableView.backgroundColor = [UIColor systemBackgroundColor];
    [self.tableView registerClass:[PostCell class] forCellReuseIdentifier:@"PostCell"];
    [self.view addSubview:self.tableView];
    
    // 自动布局
    self.tableView.translatesAutoresizingMaskIntoConstraints = NO;
    [NSLayoutConstraint activateConstraints:@[
        [self.tableView.topAnchor constraintEqualToAnchor:self.view.safeAreaLayoutGuide.topAnchor],
        [self.tableView.leadingAnchor constraintEqualToAnchor:self.view.leadingAnchor],
        [self.tableView.trailingAnchor constraintEqualToAnchor:self.view.trailingAnchor],
        [self.tableView.bottomAnchor constraintEqualToAnchor:self.view.bottomAnchor]
    ]];
}

#pragma mark - UITableViewDataSource & Delegate

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return self.posts.count;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    PostCell *cell = [tableView dequeueReusableCellWithIdentifier:@"PostCell" forIndexPath:indexPath];
    PostModel *post = self.posts[indexPath.row];
    [cell configureWithPost:post];
    return cell;
}

- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath {
    return UITableViewAutomaticDimension;
}

- (CGFloat)tableView:(UITableView *)tableView estimatedHeightForRowAtIndexPath:(NSIndexPath *)indexPath {
    return 100;
}

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    [tableView deselectRowAtIndexPath:indexPath animated:YES];
    
    PostDetailViewController *detailVC = [[PostDetailViewController alloc] init];
    detailVC.post = self.posts[indexPath.row];
    [self.navigationController pushViewController:detailVC animated:YES];
}

#pragma mark - Helper Methods

- (UIColor *)colorForAvatar:(NSString *)avatarName {
    NSDictionary *colors = @{
        @"defaultAvatar": [UIColor colorWithRed:0.8 green:0.8 blue:0.8 alpha:1],
        @"redAvatar": [UIColor colorWithRed:1.0 green:0.4 blue:0.4 alpha:1],
        @"blueAvatar": [UIColor colorWithRed:0.3 green:0.6 blue:1.0 alpha:1],
        @"greenAvatar": [UIColor colorWithRed:0.4 green:0.7 blue:0.4 alpha:1]
    };
    return colors[avatarName] ?: colors[@"defaultAvatar"];
}

#pragma mark - CreatePostDelegate
- (void)didCreateNewPost:(PostModel *)post {
    if (!self.posts) {
        self.posts = [NSMutableArray array];
    }
    [self.posts insertObject:post atIndex:0];
    
    dispatch_async(dispatch_get_main_queue(), ^{
        [self.tableView reloadData];
        if (self.posts.count > 0) {
            [self.tableView scrollToRowAtIndexPath:[NSIndexPath indexPathForRow:0 inSection:0]
                                 atScrollPosition:UITableViewScrollPositionTop
                                         animated:YES];
        }
    });
}

@end
