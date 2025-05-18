//
//  FriendsViewController.m
//  WordMaster
//
//  Created by zq z on 4/28/25.
//
#import "FriendsViewController.h"
#import "FriendModel.h"
#import "ChatViewController.h"

@interface FriendsViewController () <UITableViewDelegate, UITableViewDataSource>

@property (nonatomic, strong) UITableView *tableView;
@property (nonatomic, strong) NSMutableArray<FriendModel *> *friends;

@end

@implementation FriendsViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    self.view.backgroundColor = [UIColor whiteColor];
    [self setupTableView];
    
    self.friends = [NSMutableArray array];
    [self loadFriends];
}

- (void)setupTableView {
    self.tableView = [[UITableView alloc] initWithFrame:self.view.bounds style:UITableViewStyleInsetGrouped];
    self.tableView.dataSource = self;
    self.tableView.delegate = self;
    [self.view addSubview:self.tableView];
}

- (void)loadFriends {
    FriendModel *friend1 = [[FriendModel alloc] initWithName:@"Alice" status:@"在线"];
    FriendModel *friend2 = [[FriendModel alloc] initWithName:@"Bob" status:@"离线"];
    FriendModel *friend3 = [[FriendModel alloc] initWithName:@"Charlie" status:@"在线"];
    
    [self.friends addObjectsFromArray:@[friend1, friend2, friend3]];
    [self.tableView reloadData];
}

#pragma mark - UITableViewDataSource

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return self.friends.count;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    static NSString *CellIdentifier = @"FriendCell";
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:CellIdentifier];
    
    if (!cell) {
        cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleSubtitle reuseIdentifier:CellIdentifier];
        cell.selectionStyle = UITableViewCellSelectionStyleNone;
    }
    
    FriendModel *friend = self.friends[indexPath.row];
    
    cell.textLabel.text = friend.name;
    cell.detailTextLabel.text = friend.status;
    
    cell.accessoryType = UITableViewCellAccessoryDisclosureIndicator;
    
    return cell;
}

#pragma mark - UITableViewDelegate
// 消息按钮动作
- (void)sendMessageToFriend:(UIButton *)sender {
    NSInteger index = sender.tag;
    FriendModel *friend = self.friends[index];
    
    ChatViewController *chatVC = [[ChatViewController alloc] init];
    chatVC.friendName = friend.name;
    chatVC.messages = [self generateMockMessagesWithFriend:friend.name];
    [self.navigationController pushViewController:chatVC animated:YES];
}

// 生成模拟消息数据
- (NSMutableArray *)generateMockMessagesWithFriend:(NSString *)friendName {
    NSArray *mockMessages = @[
        @{@"sender": friendName, @"text": @"你好！最近怎么样？"},
        @{@"sender": @"我", @"text": @"还不错，你呢？"},
        @{@"sender": friendName, @"text": @"我也很好，谢谢！"},
        @{@"sender": friendName, @"text": @"有空一起学习吗？"},
        @{@"sender": @"我", @"text": @"好啊，什么时间方便？"}
    ];
    
    return [NSMutableArray arrayWithArray:mockMessages];
}

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    FriendModel *friend = self.friends[indexPath.row];
    
    ChatViewController *chatVC = [[ChatViewController alloc] init];
    chatVC.friendName = friend.name;
    chatVC.messages = [self generateMockMessagesWithFriend:friend.name];
    
    [self.navigationController pushViewController:chatVC animated:YES];
    
    // 取消选中状态
    [tableView deselectRowAtIndexPath:indexPath animated:YES];
}

@end
