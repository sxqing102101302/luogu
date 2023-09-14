import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog

def scrape_luogu(difficulty):
    # 构造URL
    url = f"https://www.luogu.com.cn/problem/list?difficulty={difficulty}"

    # 发送HTTP请求并获取页面内容
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # 解析页面内容，获取题目和题解
    problems = soup.find_all("div", class_="lg-content-item")

    # 创建markdown文件
    file_path = filedialog.asksaveasfilename(defaultextension=".md")
    with open(file_path, "w", encoding="utf-8") as f:
        # 写入题目
        f.write("# 题目列表\n\n")
        for problem in problems:
            problem_title = problem.find("a").text.strip()
            f.write(f"- {problem_title}\n")

        # 写入题解
        f.write("\n# 题解列表\n\n")
        for problem in problems:
            problem_title = problem.find("a").text.strip()
            problem_url = "https://www.luogu.com.cn" + problem.find("a")["href"]
            f.write(f"- [{problem_title}]({problem_url})\n")

def create_gui():
    # 创建窗口
    window = tk.Tk()
    window.title("洛谷题目")
    window.geometry('400x200')
    # 创建难度选择下拉菜单
    difficulty_label = tk.Label(window, text="请选择题目难度：",bg="pink",width=20,height=2)
    difficulty_label.pack()

    difficulty_var = tk.StringVar(window)
    difficulty_var.set("all")

    difficulty_menu = tk.OptionMenu(window, difficulty_var, "all", "普及-", "普及 提高-", "普及+ 提高","提高+ 省选−","省选 NOI−")
    difficulty_menu.pack()

    # 创建爬取按钮
    scrape_button = tk.Button(window, text="开始爬取", command=lambda: scrape_luogu(difficulty_var.get()))
    scrape_button.pack()

    # 运行窗口
    window.mainloop()

# 运行GUI界面
create_gui()
