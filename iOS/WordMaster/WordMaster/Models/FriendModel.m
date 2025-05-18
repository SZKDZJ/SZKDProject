//
//  FriendModel.m
//  WordMaster
//
//  Created by zq z on 4/28/25.
//

#import "FriendModel.h"

@implementation FriendModel

- (instancetype)initWithName:(NSString *)name status:(NSString *)status {
    self = [super init];
    if (self) {
        _name = name;
        _status = status;
    }
    return self;
}

@end
