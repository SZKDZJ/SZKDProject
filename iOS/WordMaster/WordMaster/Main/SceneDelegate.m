//
//  SceneDelegate.m
//  WordMaster
//
//  Created by zq z on 4/27/25.
//
#import "SceneDelegate.h"
#import "LoginViewController.h"

@implementation SceneDelegate

- (void)scene:(UIScene *)scene willConnectToSession:(UISceneSession *)session options:(UISceneConnectionOptions *)connectionOptions {

    if ([scene isKindOfClass:[UIWindowScene class]]) {
        self.window = [[UIWindow alloc] initWithWindowScene:(UIWindowScene *)scene];
        
        // 进入登录界面
        LoginViewController *loginVC = [[LoginViewController alloc] init];
        UINavigationController *nav = [[UINavigationController alloc] initWithRootViewController:loginVC];
        self.window.rootViewController = nav;
        [self.window makeKeyAndVisible];
    }
}

@end
