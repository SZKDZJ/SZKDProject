from Game.View.userView import UserView
import tkinter as tk

def main():
    # 创建 Tkinter 的 root 窗口
    root = tk.Tk()
    root.withdraw()  # 先隐藏 root 窗口
    # 初始化 UserView，传递一个空的 word_list（如果需要的话）
    user_view = UserView(word_list=None)
    # 调用登录界面
    user_view.start_view()

if __name__ == "__main__":
    main()

