import json
import os

# 用户信息文件路径
USER_FILE = os.path.join(os.path.dirname(__file__), "../db/users.json")

class UserController:
    def __init__(self):
        self.user_file = USER_FILE
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.user_file):
            with open(self.user_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_users(self):
        with open(self.user_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, indent=4, ensure_ascii=False)

    def login_user(self, account, password):
        """验证用户登录"""
        for username, user_info in self.users.items():
            if user_info["account"] == account and user_info["password"] == password:
                return username  # 返回用户名而不是用户信息
        return None

    def get_user_info(self, username):
        return self.users.get(username)

    def update_user_score(self, username, score):
        if username in self.users:
            self.users[username]['score'] += score
            self.save_users()

    def create_user(self, username, account, password):
        """创建新用户"""
        if username in self.users:
            # 用户名已存在
            return False

        # 检查账号是否已被使用
        for user in self.users.values():
            if user['account'] == account:
                return False

        # 如果一切正常，则创建新用户
        self.users[username] = {
            "account": account,
            "password": password,
            "score": 0,  # 初始得分设为0
            "wrong word book":[]
        }
        self.save_users()  # 保存新用户数据
        return True

    def update_mistakes(self, username,wrong_guesses):
        """
        更新用户的错题记录。记录某个单词的错误次数，并在两次或以上时将其添加到错题本。
        """
        for word in wrong_guesses.keys():
            if wrong_guesses.get(word)>= 2 and word not in self.users[username]['wrong word book']:
                self.users[username]['wrong word book'].append(word)
        self.save_users()

        return self.users[username]['wrong word book']

    def get_mistakes(self, username):
        return self.users[username]['wrong word book']

    def get_ranking(self, username):
        # 根据分数对用户进行排序（从高到低）
        ranked_users = sorted(self.users.items(), key=lambda item: item[1]['score'], reverse=True)
        # 构造排名列表
        ranking = [(user, data['score']) for user, data in ranked_users]
        # 获取前3名的排名
        top_3 = ranking[:3]
        # 找出指定用户的排名
        user_rank = next((idx + 1 for idx, (user, _) in enumerate(ranking) if user == username), None)
        return top_3, user_rank
