//
//  WordModel.h
//  WordMaster
//
//  Created by zq z on 4/27/25.
//

// WordModel.h
#import <Foundation/Foundation.h>

@interface WordModel : NSObject

@property (nonatomic, strong) NSString *word;
@property (nonatomic, strong) NSString *pronunciation;
@property (nonatomic, strong) NSString *definition;
@property (nonatomic, strong) NSString *audioURL;
@property (nonatomic, assign) BOOL isFavorite;

- (instancetype)initWithWord:(NSString *)word
               pronunciation:(NSString *)pronunciation
                  definition:(NSString *)definition
                    audioURL:(NSString *)audioURL;

@end
