# -*-coding:utf-8 -*-

"""
# File:         todo-list.py
# Time:         2025/8/5 14:25
# Author:       Martin
# Description:  CMD 版（文件操作）
"""
import os
import sys
from webbrowser import parse_args

"""
TOOD list

- 添加list
- 查看list
- 删除list
- 改变list
"""

TODO_FILE = 'todo.txt'


class TodoApp():
    def __init__(self, file=TODO_FILE):
        self.file = file
        self.todos = self.load_todos()

    def load_todos(self):
        if not os.path.exists(self.file):
            return []
        with open(self.file) as f:
            lines = f.readlines()
        todos = []
        for line in lines:
            if '|' in line:
                status, task = line.strip().split('|', 1)
                todos.append({'task': task, 'done': status == '1'})
        return todos

    def save_todos(self, todos):
        """
        待办保存
        :param todos:
        :return:
        """
        with open(self.file, 'w', encoding='utf-8') as f:
            for todo in todos:
                f.write(f'{int(todo['done'])}|{todo["task"]}\n')

    def list_todos(self):
        """
        待办查询
        :return:
        """
        if not self.todos:
            print("你还没有待办事项")
            return
        for idx, todo in enumerate(self.todos, start=1):
            status = "[x]" if todo['done'] else "[ ]"
            print(f'{idx}. {status} {todo["task"]}')

    def add_todo(self, task):
        self.todos.append({'task': task, 'done': False})
        self.save_todos(self.todos)
        print(f"添加成功: {task}")

    def done_todo(self, index):
        if index < 1 or index > len(self.todos):
            print("无效编码")
            return
        self.todos[index - 1]['done'] = True
        self.save_todos(self.todos)
        print(f"已完成 {self.todos[index - 1]['task']} 💕💕💕")

    def remove_todo(self, index):
        if index < 1 or index > len(self.todos):
            print("无效编码")
            return
        task = self.todos.pop(index - 1)['task']
        self.save_todos(self.todos)
        print(f"已删除 {task} 😶‍🌫️😶‍🌫️😶‍🌫️")

    def del_done_todo(self):
        # 过滤task、只保留未完成的任务
        self.todos = [todo for todo in self.todos if not todo['done']]
        self.save_todos(self.todos)
        print("已完成项已清除")

    @staticmethod
    def show_help():
        print("""
用法: python todo_app.py [命令] [参数]
命令:
    list                查看所有待办事项
    add <任务内容>       添加新任务
    done <编号>         标记任务为已完成
    remove <编号>       删除任务
    del_done           删除已完成项
    help               查看帮助
""")


def main():
    app = TodoApp()
    if len(sys.argv) < 2:
        app.show_help()
        return
    # 获取命令行第一个cmd命令参数
    cmd = sys.argv[1]
    # 获取2往后的参数
    args = sys.argv[2:]
    if cmd == 'list':
        app.list_todos()
    # 多任务添加支持
    elif cmd == 'add' and args:
        for arg in args:
            app.add_todo(arg)
    # 判断命令以及第一个参数是否为数字
    elif cmd == 'done' and args:
        indices = [int(i) for i in args if i.isdigit()]
        if indices:
            for idx in indices:
                app.done_todo(idx)
        else:
            print("请输入有效编号")
    elif cmd == 'remove' and args and args[0].isdigit():
        app.remove_todo(int(args[0]))
    elif cmd == 'del_done':
        app.del_done_todo()
    else:
        app.show_help()


if __name__ == '__main__':
    main()
