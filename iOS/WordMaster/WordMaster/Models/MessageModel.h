//
//  MessageModel.h
//  WordMaster
//
//  Created by zq z on 4/29/25.
//

#import <Foundation/Foundation.h>

@interface MessageModel : NSObject

@property (nonatomic, copy) NSString *text;
@property (nonatomic, assign) BOOL isMe;
@property (nonatomic, copy) NSString *time;

+ (instancetype)messageWithText:(NSString *)text isMe:(BOOL)isMe time:(NSString *)time;

@end
