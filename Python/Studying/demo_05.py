"""Guess the Word"""
import random

print(
    """
        欢迎参加猜单词游戏 
      把字母组合成一个正确的单词.
    """
)

# Where do the words come from?
words = ("python", "jumble", "easy",
         "difficult", "answer", "continue",
         "phone", "position", "position",
         "game")
IsContinue = 'y'
while IsContinue == 'y' or IsContinue == 'Y':
# How to randomly select words?
# 先随机挑选一个单词
    word = random.choice(words)
    correct = word # 一个用于判断玩家是否猜对的变量
    jumble ="" # 创建乱序后单词
    while word: # word不是空串时循环
        # 单词字母顺序打乱: 随机从原单词中选择一个位置，提取这个位置的字母放到新单词最后，同时删除原位置的字母，循环多次，直到原单词被抽取为空。
        position = random.randrange(len(word)) # 根据word长度，产生word的随机位置
        jumble += word[position] # 将position位置字母组合到乱序后单词
        word = word[:position] + word[(position + 1):] # 通过切片，删除原位置字母
        #另一种方法
        #l = list(word)  # 将字符串转换成列表
        #random.shuffle(l)  # 调用 random 模块的 shuffle 函数
        #jumble = ''.join(l)  # 列表转字符
    print("乱序后单词:", jumble)
    guess = input("\n请你猜: ")
    while guess != correct and guess != "":
        print("对不起不正确.")
        guess = input("继续猜: ")
    if guess == correct:
        print("真棒，你猜对了!\n")
    IsContinue=input("\n\n是否继续（Y/N)：")
