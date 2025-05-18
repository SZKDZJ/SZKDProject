//
//  MessageModel.m
//  WordMaster
//
//  Created by zq z on 4/29/25.
//

#import "MessageModel.h"

@implementation MessageModel

+ (instancetype)messageWithText:(NSString *)text isMe:(BOOL)isMe time:(NSString *)time {
    MessageModel *model = [[MessageModel alloc] init];
    model.text = text;
    model.isMe = isMe;
    model.time = time;
    return model;
}

@end
