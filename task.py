import customtkinter as ctk
from tkinter import messagebox, simpledialog
import json

class ToDoApp(ctk.CTk):
    """
    title: 上部タイトル
    geometry: ウィンドウの初期サイズ
    ctk.set_appearance_mode: 背景の色
    ctk.set_default_color_theme: ボタンの色
    """
    def __init__(self):
        super().__init__()
        self.title("ToDoリストアプリ")
        self.geometry("400x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.tasks = []  # タスクのリスト
        self.task_vars = []  # チェックボックス用の変数

        # メインフレームの作成
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(padx=10, pady=10, fill="both", expand=True)

        # スクロール可能なキャンバスフレーム
        self.canvas = ctk.CTkCanvas(self.frame)
        self.scrollbar = ctk.CTkScrollbar(self.frame, command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # ボタンの作成
        self.add_button = ctk.CTkButton(self, text="追加", command=self.add_task)
        self.add_button.pack(fill="x", padx=10, pady=2)

        self.delete_button = ctk.CTkButton(self, text="選択したタスクを削除", command=self.delete_selected_tasks)
        self.delete_button.pack(fill="x", padx=10, pady=2)

        self.save_button = ctk.CTkButton(self, text="保存", command=self.save_tasks)
        self.save_button.pack(fill="x", padx=10, pady=2)

        self.load_tasks()  # 起動時に読み込み
        self.update_task_list()  # 表示更新

    def add_task(self):
        new_task = simpledialog.askstring("タスク追加", "新しいタスクを入力してください：", parent=self)
        if new_task:
            self.tasks.append(new_task)
            self.update_task_list()

    def delete_selected_tasks(self):
        self.tasks = [task for i, task in enumerate(self.tasks) if not self.task_vars[i].get()]
        self.update_task_list()

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

    def update_task_list(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.task_vars = []
        for task in self.tasks:
            var = ctk.BooleanVar()
            chk = ctk.CTkCheckBox(self.scrollable_frame, text=task, variable=var)
            chk.pack(anchor="w", padx=5, pady=2)
            self.task_vars.append(var)
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
