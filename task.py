import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDoリストアプリ")
        self.tasks = []  # タスクのリスト

        # フレームの作成
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        # タスクリストの表示
        self.task_listbox = tk.Listbox(self.frame, selectmode=tk.SINGLE, height=10, width=50, font=("Lucida Console",12))
        self.task_listbox.pack(side=tk.LEFT, padx=5, pady=5)

        # スクロールバーの追加
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        # ボタンの作成
        self.add_button = tk.Button(root, text="追加", command=self.add_task)
        self.add_button.pack(fill=tk.X, padx=10, pady=2)

        self.delete_button = tk.Button(root, text="削除", command=self.delete_task)
        self.delete_button.pack(fill=tk.X, padx=10, pady=2)

        self.save_button = tk.Button(root, text="保存", command=self.save_tasks)
        self.save_button.pack(fill=tk.X, padx=10, pady=2)

        self.load_tasks()  # 起動時に読み込み
        self.update_task_listbox()  # 表示更新

    def add_task(self):
        new_task = simpledialog.askstring("タスク追加", "新しいタスクを入力してください：")
        if new_task:
            self.tasks.append(new_task)
            self.update_task_listbox()

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("エラー", "削除するタスクを選択してください。")

    def save_tasks(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("保存完了", "タスクを保存しました。")

    def load_tasks(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)  # リストをクリア
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)  # タスクを表示

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
