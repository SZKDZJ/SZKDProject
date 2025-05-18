//
//  ChatViewController.m
//  WordMaster
//
//  Created by zq z on 4/28/25.
//
// ChatViewController.m
#import "ChatViewController.h"
#import "MessageModel.h"

@interface ChatViewController ()
@property (nonatomic, strong) UIView *inputView;
@end

@implementation ChatViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    self.title = self.friendName;
    self.view.backgroundColor = [UIColor whiteColor];
    
    [self setupTableView];
    [self setupInputView];
    [self loadMockMessages];
}

- (void)setupTableView {
    self.tableView = [[UITableView alloc] initWithFrame:CGRectMake(0, 0, self.view.frame.size.width, self.view.frame.size.height - 50) style:UITableViewStylePlain];
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    self.tableView.separatorStyle = UITableViewCellSeparatorStyleNone;
    [self.tableView registerClass:[UITableViewCell class] forCellReuseIdentifier:@"Cell"];
    [self.view addSubview:self.tableView];
}

- (void)setupInputView {
    self.inputView = [[UIView alloc] initWithFrame:CGRectMake(0, self.view.frame.size.height - 50, self.view.frame.size.width, 50)];
    self.inputView.backgroundColor = [UIColor colorWithWhite:0.9 alpha:1.0];
    
    self.messageField = [[UITextField alloc] initWithFrame:CGRectMake(10, 10, self.view.frame.size.width - 80, 30)];
    self.messageField.borderStyle = UITextBorderStyleRoundedRect;
    self.messageField.delegate = self;
    
    self.sendButton = [UIButton buttonWithType:UIButtonTypeSystem];
    self.sendButton.frame = CGRectMake(self.view.frame.size.width - 60, 10, 50, 30);
    [self.sendButton setTitle:@"发送" forState:UIControlStateNormal];
    [self.sendButton addTarget:self action:@selector(sendMessage) forControlEvents:UIControlEventTouchUpInside];
    
    [self.inputView addSubview:self.messageField];
    [self.inputView addSubview:self.sendButton];
    [self.view addSubview:self.inputView];
}

- (void)loadMockMessages {
    self.messages = [NSMutableArray array];
    
    // 添加模拟消息
    [self.messages addObject:@{@"text": @"你好！最近怎么样？", @"isMe": @NO, @"time": @"10:00"}];
    [self.messages addObject:@{@"text": @"还不错，你呢？", @"isMe": @YES, @"time": @"10:02"}];
    [self.messages addObject:@{@"text": @"我也很好，谢谢！", @"isMe": @NO, @"time": @"10:03"}];
    
    [self.tableView reloadData];
    [self scrollToBottom];
}

// 修正后的消息高度计算方法
- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath {
    NSDictionary *message = self.messages[indexPath.row];
    NSString *text = message[@"text"];
    
    // 正确的 boundingRectWithSize 方法调用
    CGRect textRect = [text boundingRectWithSize:CGSizeMake(200, CGFLOAT_MAX)
                                        options:NSStringDrawingUsesLineFragmentOrigin
                                     attributes:@{NSFontAttributeName: [UIFont systemFontOfSize:16]}
                                        context:nil];
    
    return textRect.size.height + 30;
}

- (NSString *)currentTime {
    NSDateFormatter *formatter = [[NSDateFormatter alloc] init];
    [formatter setDateFormat:@"HH:mm"];
    return [formatter stringFromDate:[NSDate date]];
}

- (void)scrollToBottom {
    if (self.messages.count > 0) {
        NSIndexPath *indexPath = [NSIndexPath indexPathForRow:self.messages.count-1 inSection:0];
        [self.tableView scrollToRowAtIndexPath:indexPath atScrollPosition:UITableViewScrollPositionBottom animated:YES];
    }
}

#pragma mark - TableView DataSource

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return self.messages.count;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:@"Cell" forIndexPath:indexPath];
    cell.selectionStyle = UITableViewCellSelectionStyleNone;
    
    NSDictionary *message = self.messages[indexPath.row];
    BOOL isMe = [message[@"isMe"] boolValue];
    NSString *text = message[@"text"];
    NSString *time = message[@"time"];

    // 清除旧视图
    for (UIView *view in cell.contentView.subviews) {
        [view removeFromSuperview];
    }

    // 创建头像
    UIImageView *avatar = [[UIImageView alloc] initWithFrame:CGRectMake(isMe ? self.view.frame.size.width - 50 : 10, 10, 40, 40)];
    avatar.image = [UIImage imageNamed:isMe ? @"me_icon" : @"friend_icon"]; // 请添加这两个图像
    avatar.layer.cornerRadius = 20;
    avatar.layer.masksToBounds = YES;
    [cell.contentView addSubview:avatar];

    // 创建消息 Label
    UILabel *messageLabel = [[UILabel alloc] init];
    messageLabel.text = text;
    messageLabel.numberOfLines = 0;
    messageLabel.font = [UIFont systemFontOfSize:16];
    messageLabel.textColor = isMe ? [UIColor whiteColor] : [UIColor blackColor];

    // 计算文本尺寸
    CGSize maxSize = CGSizeMake(self.view.frame.size.width * 0.6, CGFLOAT_MAX);
    CGRect textRect = [text boundingRectWithSize:maxSize
                                          options:NSStringDrawingUsesLineFragmentOrigin
                                       attributes:@{NSFontAttributeName: [UIFont systemFontOfSize:16]}
                                          context:nil];

    // 创建包裹气泡 View
    UIView *bubbleView = [[UIView alloc] initWithFrame:CGRectMake(0, 10, textRect.size.width + 20, textRect.size.height + 20)];
    bubbleView.backgroundColor = isMe ? [UIColor colorWithRed:0.1 green:0.5 blue:1.0 alpha:1.0] : [UIColor colorWithWhite:0.9 alpha:1.0];
    bubbleView.layer.cornerRadius = 15;
    bubbleView.layer.masksToBounds = YES;

    messageLabel.frame = CGRectMake(10, 10, textRect.size.width, textRect.size.height);
    [bubbleView addSubview:messageLabel];

    // 设置位置
    CGFloat bubbleX = isMe ? self.view.frame.size.width - bubbleView.frame.size.width - 60 : 60;
    bubbleView.frame = CGRectMake(bubbleX, 10, bubbleView.frame.size.width, bubbleView.frame.size.height);
    [cell.contentView addSubview:bubbleView];

    // 添加时间戳
    UILabel *timeLabel = [[UILabel alloc] initWithFrame:CGRectMake(bubbleX, CGRectGetMaxY(bubbleView.frame) + 5, 120, 15)];
    timeLabel.text = time;
    timeLabel.font = [UIFont systemFontOfSize:12];
    timeLabel.textColor = [UIColor grayColor];
    [cell.contentView addSubview:timeLabel];

    return cell;
}

@end
