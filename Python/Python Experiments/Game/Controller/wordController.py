import random
import os

class WordController:
    def __init__(self, word_list=None):
        if word_list is None:
            word_list = []
        self.word_list = [word.strip().lower() for word in word_list]
        self.wrong_guesses = {} # 跟踪猜错次数
        self.current_word = None
        self.guess_attempts = {}  # 记录每个单词的猜测次数

    @staticmethod
    def word_Shuffle(word):
        """
        将传入的单词打乱顺序
        避免打乱后的单词与原始单词相同
        """
        word_letters = list(word)
        while True:
            random.shuffle(word_letters)
            jumble = ''.join(word_letters)
            if jumble != word:  # 确保打乱后的单词与原始单词不同
                return jumble

    def get_random_word(self):
        """从单词列表中随机抽取一个单词"""
        if not self.word_list:
            raise ValueError("单词列表为空")
        word0 = random.choice(self.word_list)
        return word0

    def word_Compare(self, user_word, list_word):
        if user_word.strip().lower() == list_word.strip().lower():
            return True
        else:
            if list_word not in self.wrong_guesses:
                # 如果单词不在字典中，先将其初始化为 0
                self.wrong_guesses[list_word] = 0
            self.wrong_guesses[list_word] += 1  # 猜错次数 +1
            return False

    def next_word(self):
        if not self.word_list:
            print("所有单词已被猜对！")
            exit()

        # 增加猜错次数高的单词的权重
        self.word_list = self.word_list + [word for word, count in self.wrong_guesses.items() if count > 0]

        word0 = self.get_random_word()
        word1 = self.word_Shuffle(word0)
        self.current_word = word0
        return word0, word1

    def add_word(self, word):
        """
        动态添加单词到列表
        """
        word = word.strip().lower()
        if word not in self.word_list:
            self.word_list.append(word)
            return True
        else:
            return False

    def remove_word(self, word):
        word = word.strip().lower()
        if word in self.word_list:
            for i in range(len(self.word_list)):
                self.word_list.remove(word)
                if word not in self.word_list:
                    break
            return True
        else:
            print(f"单词 '{word}' 不存在于列表中。")
            return False

    def import_word(self, choose,file_path):
        """
        根据用户选择导入单词列表
        """
        if choose == '1':
            try:
                with open(os.path.join(os.path.dirname(__file__), "../db/Word_List1.txt"), encoding='utf-8') as Word_List:
                    word_list = Word_List.readlines()
                    if word_list:
                        self.word_list = [word.strip().lower() for word in word_list]
                        print(f"成功导入 {len(self.word_list)} 个单词。")
                    else:
                        print("文件中没有任何单词。")
            except FileNotFoundError:
                print("文件未找到，请检查文件路径。")
        elif choose == '2':
            try:
                with open(os.path.join(os.path.dirname(__file__), "../db/Word_List2.txt"), encoding='utf-8') as Word_List:
                    word_list = Word_List.readlines()
                    if word_list:
                        self.word_list = [word.strip().lower() for word in word_list]
                        print(f"成功导入 {len(self.word_list)} 个单词。")
                    else:
                        print("文件中没有任何单词。")
            except FileNotFoundError:
                print("文件未找到，请检查文件路径。")
        elif choose == '3':  # 提示用户输入文件路径
            try:
                with open(file_path, encoding='utf-8') as Word_List:
                    word_list = Word_List.readlines()
                self.word_list = [word.strip().lower() for word in word_list]
                print(f"成功导入 {len(self.word_list)} 个单词。")
                return True
            except FileNotFoundError:
                print("文件未找到，请检查文件路径。")
                return False

    def track_attempts(self):
        # 记录猜测次数并决定是否移除单词
        self.guess_attempts[self.current_word] += 1
        if self.guess_attempts[self.current_word] == 2:
            self.remove_word(self.current_word)


