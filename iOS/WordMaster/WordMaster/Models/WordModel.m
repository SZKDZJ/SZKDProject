//
//  WordModel.m
//  WordMaster
//
//  Created by zq z on 4/27/25.
//
// WordModel.m
#import "WordModel.h"
#import "UserManager.h"

@implementation WordModel

- (instancetype)initWithWord:(NSString *)word
               pronunciation:(NSString *)pronunciation
                  definition:(NSString *)definition
                    audioURL:(NSString *)audioURL {
    self = [super init];
    if (self) {
        _word = word;
        _pronunciation = pronunciation;
        _definition = definition;
        _audioURL = audioURL;
        _isFavorite = [[UserManager sharedManager] isWordFavorited:word];
    }
    return self;
}

@end
