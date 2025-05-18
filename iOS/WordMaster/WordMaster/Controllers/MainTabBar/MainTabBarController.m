//
//  MainTabBarController.m
//  WordMaster
//
//  Created by zq z on 4/27/25.
//
// MainTabBarController.m
#import "MainTabBarController.h"
#import "LearnViewController.h"
#import "CommunityViewController.h"
#import "ProfileViewController.h"

@implementation MainTabBarController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    // 创建 LearnViewController 实例
    LearnViewController *learnVC = [[LearnViewController alloc] init];
    UINavigationController *learnNav = [[UINavigationController alloc] initWithRootViewController:learnVC];
    learnNav.tabBarItem.title = @"学习";
    learnNav.tabBarItem.image = [UIImage systemImageNamed:@"book"];
    
    // 创建 CommunityViewController 实例
    CommunityViewController *communityVC = [[CommunityViewController alloc] init];
    UINavigationController *communityNav = [[UINavigationController alloc] initWithRootViewController:communityVC];
    communityNav.tabBarItem.title = @"社区";
    communityNav.tabBarItem.image = [UIImage systemImageNamed:@"person.2"];
    
    // 创建 ProfileViewController 实例
    ProfileViewController *profileVC = [[ProfileViewController alloc] init];
    UINavigationController *profileNav = [[UINavigationController alloc] initWithRootViewController:profileVC];
    profileNav.tabBarItem.title = @"个人";
    profileNav.tabBarItem.image = [UIImage systemImageNamed:@"person.circle"];
    
    self.viewControllers = @[learnNav, communityNav, profileNav];
    
    // 扁平风格 TabBar 美化
    self.tabBar.tintColor = [UIColor systemBlueColor];
    self.tabBar.backgroundColor = [UIColor whiteColor];
}

@end
