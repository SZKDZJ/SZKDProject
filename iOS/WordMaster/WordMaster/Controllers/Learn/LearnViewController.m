//
//  LearnViewController.m
//  WordMaster
//
//  Created by zq z on 4/27/25.
//

#import "LearnViewController.h"
#import "WordModel.h"
#import "WordDetailViewController.h"
#import "UserManager.h"

@interface LearnViewController () <UITableViewDelegate, UITableViewDataSource, UISearchBarDelegate>

@property (nonatomic, strong) UITableView *tableView;
@property (nonatomic, strong) UISearchBar *searchBar;
@property (nonatomic, strong) NSArray<WordModel *> *words;          // 全部单词
@property (nonatomic, strong) NSArray<WordModel *> *filteredWords;   // 搜索后的单词
@property (nonatomic, strong) NSMutableSet *learnedWords;            // 已学单词
@property (nonatomic, assign) BOOL isSearching;

@end

@implementation LearnViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    self.title = @"学习";
    self.view.backgroundColor = [UIColor systemGroupedBackgroundColor];
    
    self.learnedWords = [NSMutableSet set];
    [self setupNavigationBar];
    [self setupTableView];
    [self loadWordsFromJSON];
}

#pragma mark - 初始化界面

- (void)setupNavigationBar {
    UIBarButtonItem *randomButton = [[UIBarButtonItem alloc] initWithTitle:@"随机学习"
                                            style:UIBarButtonItemStylePlain
                                                        target:self
                                        action:@selector(startRandomLearning)];
    self.navigationItem.rightBarButtonItem = randomButton;
}

- (void)setupTableView {
    self.tableView = [[UITableView alloc] initWithFrame:CGRectZero style:UITableViewStylePlain];
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    [self.tableView registerClass:[UITableViewCell class] forCellReuseIdentifier:@"WordCell"];
    self.tableView.translatesAutoresizingMaskIntoConstraints = NO;
    [self.view addSubview:self.tableView];
    
    // 自动布局：让 tableView 贴满整个界面（包括 Safe Area）
    [NSLayoutConstraint activateConstraints:@[
        [self.tableView.topAnchor constraintEqualToAnchor:self.view.safeAreaLayoutGuide.topAnchor],
        [self.tableView.bottomAnchor constraintEqualToAnchor:self.view.safeAreaLayoutGuide.bottomAnchor],
        [self.tableView.leadingAnchor constraintEqualToAnchor:self.view.leadingAnchor],
        [self.tableView.trailingAnchor constraintEqualToAnchor:self.view.trailingAnchor]
    ]];
    
    // 设置搜索栏
    self.searchBar = [[UISearchBar alloc] init];
    self.searchBar.delegate = self;
    self.searchBar.placeholder = @"搜索单词";
    self.tableView.tableHeaderView = self.searchBar;
}

- (void)loadWordsFromJSON {
    NSString *path = [[NSBundle mainBundle] pathForResource:@"words" ofType:@"json"];
    NSData *data = [NSData dataWithContentsOfFile:path];
    if (!data) {
        NSLog(@"❌ 没找到 words.json 文件");
        return;
    }
    
    NSError *error;
    NSArray *jsonArray = [NSJSONSerialization JSONObjectWithData:data options:kNilOptions error:&error];
    if (error) {
        NSLog(@"❌ JSON解析失败：%@", error.localizedDescription);
        return;
    }
    
    NSMutableArray *tempArray = [NSMutableArray array];
    for (NSDictionary *dict in jsonArray) {
        WordModel *model = [[WordModel alloc] initWithWord:dict[@"word"]
                                             pronunciation:dict[@"pronunciation"]
                                                definition:dict[@"definition"]
                                                  audioURL:dict[@"audioURL"]];
        [tempArray addObject:model];
    }
    self.words = tempArray;
    self.filteredWords = self.words;
    
    [self.tableView reloadData];
}

#pragma mark - UITableViewDelegate & DataSource

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return self.filteredWords.count;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:@"WordCell" forIndexPath:indexPath];
    
    WordModel *model = self.filteredWords[indexPath.row];
    cell.textLabel.text = model.word;
    
    // 显示已学打勾
    if ([self.learnedWords containsObject:model.word]) {
        cell.accessoryType = UITableViewCellAccessoryCheckmark;
    } else {
        cell.accessoryType = UITableViewCellAccessoryNone;
    }
    
    return cell;
}

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    [tableView deselectRowAtIndexPath:indexPath animated:YES];
    
    WordModel *model = self.filteredWords[indexPath.row];
    
    // 标记为已学
    [self.learnedWords addObject:model.word];

    // 更新当前用户的学习记录
    UserManager *manager = [UserManager sharedManager];
    UserModel *user = [manager getCurrentUser];

    // 如果该词第一次学，才计入学习数
    if (![user.learnedWords containsObject:model.word]) {
        [user.learnedWords addObject:model.word];
        user.learnedWordsCount = user.learnedWords.count;
        [manager saveUsers]; // 保存修改
    }

    [self.tableView reloadData];
    
    WordDetailViewController *detailVC = [[WordDetailViewController alloc] initWithWord:model];
    [self.navigationController pushViewController:detailVC animated:YES];
}

#pragma mark - 搜索

- (void)searchBar:(UISearchBar *)searchBar textDidChange:(NSString *)searchText {
    if (searchText.length == 0) {
        self.filteredWords = self.words;
        self.isSearching = NO;
    } else {
        self.isSearching = YES;
        NSPredicate *predicate = [NSPredicate predicateWithFormat:@"word CONTAINS[cd] %@", searchText];
        self.filteredWords = [self.words filteredArrayUsingPredicate:predicate];
    }
    [self.tableView reloadData];
}

- (void)searchBarCancelButtonClicked:(UISearchBar *)searchBar {
    self.isSearching = NO;
    self.searchBar.text = @"";
    [self.searchBar resignFirstResponder];
    self.filteredWords = self.words;
    [self.tableView reloadData];
}

#pragma mark - 随机学习

- (void)startRandomLearning {
    if (self.filteredWords.count == 0) return;
    
    NSUInteger randomIndex = arc4random_uniform((uint32_t)self.filteredWords.count);
    WordModel *randomWord = self.filteredWords[randomIndex];
    
    WordDetailViewController *detailVC = [[WordDetailViewController alloc] initWithWord:randomWord];
    [self.navigationController pushViewController:detailVC animated:YES];
}

@end
