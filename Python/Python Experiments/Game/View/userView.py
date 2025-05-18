import tkinter as tk
from tkinter import messagebox
from Game.Controller.userController import UserController
from Game.Controller.wordController import WordController

class UserView:
    def __init__(self, word_list):
        if word_list is None:
            word_list = []
        self.word_list = word_list
        self.user_controller = UserController()
        self.word_controller = WordController(self.word_list)
        self.username = None
        self.current_word = None

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        window.geometry(f"{width}x{height}+{position_right}+{position_top}")

    def start_view(self):
        # 主选择窗口
        self.root = tk.Tk()
        self.root.title("欢迎")

        # 显示在屏幕中央
        self.center_window(self.root, 400, 400)

        self.root.configure(background='aliceblue')

        # 创建一个框架容纳控件，使其在窗口中居中
        frame = tk.Frame(self.root, bg="aliceblue")
        frame.pack(expand=True)

        tk.Label(frame, text="欢迎，来到猜单词游戏！",fg='cadetblue',bg='aliceblue',
                 font=('STXinwei',20)).pack(pady=20)

        tk.Label(frame, text="请选择操作",fg='cadetblue',bg='aliceblue',
                 font=('STXinwei',20)).pack(pady=10)

        tk.Button(frame, text="登录", command=self.login_user_view,
                  fg='steelblue',bg='ghostwhite',font=('STKaiti',15)).pack(pady=10)
        tk.Button(frame, text="创建账号", command=self.create_account_view,
                  fg='steelblue',bg='ghostwhite',font=('STKaiti',15)).pack(pady=10)

        self.root.mainloop()

    def login_user_view(self):
        # 登录窗口 (取消用户名输入框)
        self.root.destroy()  # 关闭选择窗口
        self.login_user_v = tk.Tk()
        self.login_user_v.title("登录")

        self.center_window(self.login_user_v, 400, 400)
        self.login_user_v.configure(background='aliceblue')

        # 创建一个框架容纳控件，使其在窗口中居中
        frame = tk.Frame(self.login_user_v, bg="aliceblue")
        frame.pack(expand=True)

        # 账号标签和输入框
        tk.Label(frame, text="账号：", bg="aliceblue",
                 fg='cadetblue',font=('STXinwei',20)).grid(row=0, column=0, pady=5, sticky="e")  # 右对齐标签
        self.account_entry = tk.Entry(frame)
        self.account_entry.grid(row=0, column=1, pady=5, sticky="w")  # 左对齐输入框

        # 密码标签和输入框
        tk.Label(frame, text="密码：", bg="aliceblue",
                 fg='cadetblue',font=('STXinwei',20)).grid(row=1, column=0, pady=5, sticky="e")  # 右对齐标签
        self.password_entry = tk.Entry(frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, sticky="w")  # 左对齐输入框

        # 登录按钮
        tk.Button(frame, text="登录", command=self.login_user,
                  fg='steelblue',bg='ghostwhite',font=('STKaiti',15)
                  ).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(frame, text="返回", command=self.login_return,
                  fg='steelblue',bg='ghostwhite',font=('STKaiti',15)
                  ).grid(row=3, column=0, columnspan=2, pady=10)

        self.login_user_v.mainloop()

    def login_return(self):
        self.login_user_v.destroy()
        self.start_view()

    def create_account_view(self):
        # 创建账号窗口
        self.root.destroy()  # 关闭选择窗口
        self.root = tk.Tk()
        self.root.title("创建账号")

        self.center_window(self.root, 400, 400)
        self.root.configure(background='aliceblue')

        # 创建一个框架容纳控件，使其在窗口中居中
        frame = tk.Frame(self.root, bg="aliceblue")
        frame.pack(expand=True)

        # 用户名标签和输入框
        tk.Label(frame, text="用户名：", bg="aliceblue",
                 fg='cadetblue', font=('STXinwei', 20)).grid(row=0, column=0, pady=10, sticky="e")
        self.username_entry = tk.Entry(frame)
        self.username_entry.grid(row=0, column=1, pady=10, sticky="w")

        # 账号标签和输入框
        tk.Label(frame, text="账号：", bg="aliceblue",
                 fg='cadetblue', font=('STXinwei', 20)).grid(row=1, column=0, pady=10, sticky="e")
        self.account_entry = tk.Entry(frame)
        self.account_entry.grid(row=1, column=1, pady=10, sticky="w")

        # 密码标签和输入框
        tk.Label(frame, text="密码：", bg="aliceblue",
                 fg='cadetblue', font=('STXinwei', 20)).grid(row=2, column=0, pady=10, sticky="e")
        self.password_entry = tk.Entry(frame, show="*")
        self.password_entry.grid(row=2, column=1, pady=10, sticky="w")

        # 创建账号按钮
        tk.Button(frame, text="创建账号", command=self.create_account,
                  fg='steelblue', bg='ghostwhite', font=('STKaiti', 15)
                  ).grid(row=3, column=0, columnspan=2, pady=20)

        tk.Button(frame, text="返回", command=self.create_return,
                  fg='steelblue',bg='ghostwhite',font=('STKaiti',15)
                  ).grid(row=4, column=0, columnspan=2, pady=10)

        self.root.mainloop()

    def create_return(self):
        self.root.destroy()
        self.start_view()

    def create_account(self):
        # 处理创建账号逻辑
        username = self.username_entry.get().strip()
        account = self.account_entry.get().strip()
        password = self.password_entry.get().strip()

        if username and account and password:
            success = self.user_controller.create_user(username, account, password)
            if success:
                messagebox.showinfo("创建成功", f"账号 {account} 创建成功！")
                self.root.destroy()  # 关闭创建账号窗口
                self.start_view()  # 返回选择界面
            else:
                messagebox.showerror("创建失败", "账号或用户名已存在，请选择其他账号或用户名！")
        else:
            messagebox.showwarning("输入错误", "请输入完整的信息！")

    def login_user(self):
        # 处理用户登录逻辑
        account = self.account_entry.get().strip()
        password = self.password_entry.get().strip()

        username = self.user_controller.login_user(account, password)  # 只需账号和密码
        if username:  # 如果返回的不是 None，表示登录成功
            self.username = username  # 存储用户名
            messagebox.showinfo("登录成功", f"欢迎 {username}！")  # 显示真正的用户名
            self.login_user_v.destroy()  # 关闭登录窗口
            self.show_menu()  # 显示主菜单
        else:
            messagebox.showerror("登录失败", "账号或密码错误，请重试。")

    def show_menu(self):
        # 显示主菜单
        self.menu_root = tk.Tk()
        self.menu_root.title("主菜单")
        self.center_window(self.menu_root, 400, 400)
        self.menu_root.configure(background='aliceblue')

        # 创建一个框架容纳控件，使其在窗口中居中
        frame = tk.Frame(self.menu_root, bg="aliceblue")
        frame.pack(expand=True)

        tk.Label(frame, text=f'欢迎，{self.username}',fg='cadetblue',bg='aliceblue',
                 font=('STXinwei',20)).pack(pady=20)

        tk.Button(frame, text="导入单词表", fg='steelblue',bg='ghostwhite',font=('STKaiti',15)
                  , command=self.menu_to_import).pack(pady=10)
        tk.Button(frame, text="开始游戏",
                  fg='steelblue',bg='ghostwhite',font=('STKaiti',15),command=self.start_game).pack(pady=10)
        tk.Button(frame, text="查询个人信息", fg='steelblue',
                  bg='ghostwhite',font=('STKaiti',15),command=self.consult_user_to_import).pack(pady=10)
        tk.Button(frame, text="查询排名榜", fg='steelblue',
                  bg='ghostwhite', font=('STKaiti', 15), command=self.menu_to_rank).pack(pady=10)
        tk.Button(frame, text="注销", fg='steelblue',
                  bg='ghostwhite', font=('STKaiti', 15), command=self.menu_to_start).pack(pady=10)

        self.menu_root.mainloop()

    def menu_to_start(self):
        self.menu_root.destroy()
        self.start_view()

    def menu_to_import(self):
        self.menu_root.destroy()
        self.import_word_view()

    def menu_to_rank(self):
        self.menu_root.destroy()
        self.rankingLists()

    def import_word_view(self):
        # 导入单词表功能
        self.import_word = tk.Tk()
        self.import_word.title("导入单词表")
        self.center_window(self.import_word, 400, 400)
        self.import_word.configure(background='aliceblue')

        # 创建一个框架容纳控件，使其在窗口中居中
        frame = tk.Frame(self.import_word, bg="aliceblue")
        frame.pack(expand=True)

        tk.Button(frame, text="四级单词",
                  fg='steelblue', bg='ghostwhite', font=('STKaiti', 15),command=self.import_word_1).pack(pady=10)
        tk.Button(frame, text="六级单词",
                  fg='steelblue', bg='ghostwhite', font=('STKaiti', 15),command=self.import_word_2).pack(pady=10)
        tk.Button(frame, text="导入个人单词表",
                  fg='steelblue', bg='ghostwhite', font=('STKaiti', 15),command=self.import_word_3).pack(pady=10)
        tk.Button(frame, text="增加单词",
                  fg='steelblue', bg='ghostwhite', font=('STKaiti', 15),command=self.add_word_view).pack(pady=10)
        tk.Button(frame, text="删除单词",
                  fg='steelblue', bg='ghostwhite', font=('STKaiti', 15),command=self.remove_word_view).pack(pady=10)
        tk.Button(frame, text="返回主菜单",
                  fg='steelblue', bg='ghostwhite', font=('STKaiti', 15), command=self.import_return_menu).pack(pady=10)

        self.import_word.mainloop()

    #导入界面返回主菜单
    def import_return_menu(self):
        self.import_word.destroy()
        self.show_menu()

    # 导入单词的具体实现
    def import_word_1(self):
        self.word_controller.import_word('1', None)
        messagebox.showinfo("导入成功", f"成功导入四级单词！")

    def import_word_2(self):
        self.word_controller.import_word('2', None)
        messagebox.showinfo("导入成功", f"成功导入六级单词！")

    def import_word_3(self):
        """导入个人单词表"""
        self.import_word.destroy()
        self.import_word_3_window = tk.Tk()
        self.import_word_3_window.title("导入个人单词表")

        self.center_window(self.import_word_3_window, 400, 400)
        self.import_word_3_window.configure(background='aliceblue')

        # 创建一个框架容纳控件，使其在窗口中居中
        frame = tk.Frame(self.import_word_3_window, bg="aliceblue")
        frame.pack(expand=True)

        # 文件路径标签和输入框
        tk.Label(frame, text="请输入文件路径：",
                 bg="aliceblue",fg='cadetblue', font=('STXinwei', 20)
                 ).grid(row=0, column=0, pady=5, sticky="e")
        self.file_path_entry = tk.Entry(frame, width=30)
        self.file_path_entry.grid(row=1, column=0, pady=10, sticky="w")

        # 导入按钮
        tk.Button(frame, text="导入",
                  fg='steelblue',bg='ghostwhite',font=('STKaiti',15),
                  command=self.submit_import_word_3
                  ).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(frame, text="返回",
                  fg='steelblue',bg='ghostwhite',font=('STKaiti',15),
                  command=self.word3_to_import
                  ).grid(row=3, column=0, columnspan=2, pady=10)

        self.import_word_3_window.mainloop()

    def word3_to_import(self):
        self.import_word_3_window.destroy()
        self.import_word_view()

    def submit_import_word_3(self):
        """处理导入个人单词表"""
        file_path = self.file_path_entry.get().strip()
        if file_path:
            try:
                sign = self.word_controller.import_word('3', file_path)
                if sign == True:
                    messagebox.showinfo("导入成功", "单词表导入成功！")
                else:
                    messagebox.showerror("导入失败", f"导入失败,请输入有效的文件路径。")
            except Exception as e:
                messagebox.showerror("导入失败", f"导入失败: {str(e)}")
        else:
            messagebox.showwarning("输入错误", "请输入有效的文件路径。")
        self.import_word_3_window.destroy()
        self.import_word_view()

    # 增加和删除单词的功能
    def add_word_view(self):
        # 增加单词窗口
        self.import_word.destroy()
        self.add_word_window = tk.Tk()
        self.add_word_window.title("增加单词")
        self.center_window(self.add_word_window, 400, 400)
        self.add_word_window.configure(background='aliceblue')

        # 创建一个框架容纳控件，使其在窗口中居中
        frame = tk.Frame(self.add_word_window, bg="aliceblue")
        frame.pack(expand=True)

        tk.Label(frame, text="输入需要增加的单词：",
                 bg="aliceblue", fg='cadetblue', font=('STXinwei', 20)
                 ).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.add_word_entry = tk.Entry(frame,width=20)
        self.add_word_entry.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        tk.Button(frame, text="提交",
                  fg='steelblue', bg='ghostwhite', font=('STKaiti', 15),
                  command=self.submit_add_word).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(frame, text="返回",
                  fg='steelblue',bg='ghostwhite',font=('STKaiti',15),
                  command=self.add_word_to_import
                  ).grid(row=3, column=0, columnspan=2, pady=10)

        self.add_word_window.mainloop()

    def add_word_to_import(self):
        self.add_word_window.destroy()
        self.import_word_view()

    def submit_add_word(self):
        word = self.add_word_entry.get().strip()
        if word:
            if self.word_controller.add_word(word):
                messagebox.showinfo("成功", f"成功增加单词: {word}")
            else:
                messagebox.showinfo("失败", f"单词 {word} 已存在列表")
        else:
            messagebox.showwarning("错误", "请输入有效的单词。")

        self.add_word_entry.delete(0, tk.END)  # 清空输入框

    def remove_word_view(self):
        # 删除单词窗口
        self.import_word.destroy()
        self.remove_word_window = tk.Tk()
        self.remove_word_window.title("删除单词")
        self.center_window(self.remove_word_window, 400, 400)
        self.remove_word_window.configure(background='aliceblue')

        # 创建一个框架容纳控件，使其在窗口中居中
        frame = tk.Frame(self.remove_word_window, bg="aliceblue")
        frame.pack(expand=True)

        tk.Label(frame, text="输入需要删除的单词：",
                 bg="aliceblue", fg='cadetblue', font=('STXinwei', 20)
                 ).grid(row=0, column=0, padx=10, pady=10,sticky="e")
        self.remove_word_entry = tk.Entry(frame,width=20)
        self.remove_word_entry.grid(row=1, column=0, padx=10, pady=10,sticky="w")

        tk.Button(frame, text="提交",
                  fg='steelblue', bg='ghostwhite', font=('STKaiti', 15),
                  command=self.submit_remove_word).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(frame, text="返回",
                  fg='steelblue',bg='ghostwhite',font=('STKaiti',15),
                  command=self.remove_word_to_import
                  ).grid(row=3, column=0, columnspan=2, pady=10)

        self.remove_word_window.mainloop()

    def remove_word_to_import(self):
        self.remove_word_window.destroy()
        self.import_word_view()

    def submit_remove_word(self):
        word = self.remove_word_entry.get().strip()
        if word:
            if self.word_controller.remove_word(word):
                messagebox.showinfo("成功", f"成功删除单词: {word}")
            else:
                messagebox.showinfo("失败", f"列表中没有单词 {word}")
        else:
            messagebox.showwarning("错误", "请输入有效的单词。")

        self.remove_word_entry.delete(0, tk.END)  # 清空输入框

    def start_game(self):
        # 开始游戏并显示游戏界面
        if self.word_controller.word_list:
            self.menu_root.destroy()
            self.root = tk.Tk()
            self.root.title("单词游戏")
            self.center_window(self.root, 400, 400)
            self.root.configure(background='aliceblue')

            # 创建一个框架容纳控件，使其在窗口中居中
            frame = tk.Frame(self.root, bg="aliceblue")
            frame.pack(expand=True)

            self.score_label = tk.Label(frame,
                                        fg='cadetblue', bg='aliceblue',font=('STXinwei', 17),
                                        text=f"当前得分: {self.user_controller.get_user_info(self.username)['score']}")
            self.score_label.pack(pady=10)

            self.word_label = tk.Label(frame, text="")
            self.word_label.pack(pady=10)

            self.guess_entry = tk.Entry(frame)
            self.guess_entry.pack(pady=10)

            tk.Button(frame, text="提交", command=self.check_guess,
                      fg='steelblue',bg='ghostwhite',font=('STKaiti',15)).pack(pady=10)

            tk.Button(frame, text="跳过", command=self.next_word,
                      fg='steelblue',bg='ghostwhite',font=('STKaiti',15)).pack(pady=10)

            tk.Button(frame, text="返回主菜单", command=self.exit_to_menu,
                      fg='steelblue',bg='ghostwhite',font=('STKaiti',15)).pack(pady=10)

            self.next_word()
        else:
            messagebox.showerror("单词表为空", "请先导入单词表！")

    def next_word(self):
        # 获取并展示下一个乱序单词
        if not self.word_controller.word_list:
            messagebox.showinfo("完成", "所有单词已猜完！")
            self.root.destroy()
            self.show_menu()
            return

        word0, word1 = self.word_controller.next_word()
        self.current_word = word0
        self.word_label.config(text=f"乱序单词: {word1}",fg='cadetblue',bg='aliceblue',
                 font=('STXinwei',20))
        if self.current_word not in self.word_controller.guess_attempts:
            self.word_controller.guess_attempts[self.current_word] = 0

        if self.guess_entry:
            self.guess_entry.delete(0, tk.END)  # 清空输入框

    def check_guess(self):
        # 检查用户输入的猜测
        guess = self.guess_entry.get().strip().lower()
        if self.word_controller.word_Compare(guess, self.current_word):
            messagebox.showinfo("结果", "猜对了！")
            self.update_score()
            self.word_controller.track_attempts()
            self.next_word()
        else:
            messagebox.showerror("结果", "猜错了！")
            self.guess_entry.delete(0, tk.END)  # 清空输入框
            wrong_guesses = self.word_controller.wrong_guesses
            self.user_controller.update_mistakes(self.username,wrong_guesses)

    def exit_to_menu(self):
        """退出游戏并返回主菜单"""
        if messagebox.askyesno("退出", "确定要退出游戏并返回主菜单吗？"):
            self.root.destroy()  # 关闭游戏窗口
            self.show_menu()  # 返回主菜单

    def update_score(self):
        # 更新得分逻辑
        attempts = self.word_controller.guess_attempts[self.current_word]
        if attempts == 0:
            self.user_controller.update_user_score(self.username, 3)
        elif attempts == 1:
            self.user_controller.update_user_score(self.username, 1)
        self.score_label.config(text=f"当前得分: {self.user_controller.get_user_info(self.username)['score']}")

    def consult_user_to_import(self):
        self.menu_root.destroy()
        self.consult_user()

    def consult_user(self):
        self.consult_user_window = tk.Tk()
        self.consult_user_window.title("查询个人信息")
        self.center_window(self.consult_user_window, 400, 400)
        self.consult_user_window.configure(background='aliceblue')

        # 创建一个框架容纳控件，使其在窗口中居中
        frame = tk.Frame(self.consult_user_window, bg="aliceblue")
        frame.pack(expand=True)

        tk.Label(frame, text=f"用户名: {self.username}\n"
                             f"得分: {self.user_controller.get_user_info(self.username)['score']}",
                 fg='cadetblue', bg='aliceblue',font=('STXinwei', 20)).pack(pady=20)

        tk.Button(frame, text='查询错题本', fg='steelblue', bg='ghostwhite', font=('STKaiti', 15)
                  , command=self.wrong_word_book).pack(pady=10)
        tk.Button(frame, text='返回', fg='steelblue', bg='ghostwhite', font=('STKaiti', 15)
                  , command=self.consult_user_to_menu).pack(pady=10)

        self.consult_user_window.mainloop()

    def consult_user_to_menu(self):
        self.consult_user_window.destroy()
        self.show_menu()

    def wrong_word_book(self):
        self.consult_user_window.destroy()
        self.consult_wrong = tk.Tk()
        self.consult_wrong.title("错题本")
        self.center_window(self.consult_wrong, 400, 400)
        self.consult_wrong.configure(background='aliceblue')

        # 创建一个框架容纳控件，使其在窗口中居中
        frame = tk.Frame(self.consult_wrong, bg="aliceblue")
        frame.pack(expand=True)

        tk.Label(frame, text='错题本',
                 fg='cadetblue', bg='aliceblue', font=('STXinwei', 17)).pack(pady=20)
        tk.Label(frame, text=f'{self.user_controller.get_mistakes(self.username)}',
                 fg='cadetblue', bg='aliceblue', font=('STXinwei', 17)).pack(pady=20)

        tk.Button(frame, text='返回', fg='steelblue', bg='ghostwhite', font=('STKaiti', 15)
                  , command=self.consult_word_to_user).pack(pady=10)

        self.consult_wrong.mainloop()

    def consult_word_to_user(self):
        self.consult_wrong.destroy()
        self.consult_user()

    def rankingLists(self):
        self.rankingLists_window = tk.Tk()
        self.rankingLists_window.title("排行榜")
        self.center_window(self.rankingLists_window, 400, 400)
        self.rankingLists_window.configure(background='aliceblue')

        # 创建一个框架容纳控件，使其在窗口中居中
        frame = tk.Frame(self.rankingLists_window, bg="aliceblue")
        frame.pack(expand=True)

        tk.Label(frame, text='排行榜',
                 fg='cadetblue', bg='aliceblue', font=('STXinwei', 17)).pack(pady=20)

        ranking, user_rank = self.user_controller.get_ranking(self.username)
        for idx, (user, score) in enumerate(ranking, 1):
            tk.Label(frame, text=f"排名 {idx}: {user} - {score} 分\n",
                     fg='cadetblue', bg='aliceblue', font=('STXinwei', 15)).pack(pady=8)

        tk.Label(frame, text=f'{self.username} 的排名: 第 {user_rank} 名',
                 fg='cadetblue', bg='aliceblue', font=('STXinwei', 15)).pack(pady=8)

        tk.Button(frame, text='返回', fg='steelblue', bg='ghostwhite', font=('STKaiti', 15)
                  , command=self.rankingLists_to_user).pack(pady=10)

        self.rankingLists_window.mainloop()

    def rankingLists_to_user(self):
        self.rankingLists_window.destroy()
        self.show_menu()