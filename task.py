import customtkinter as ctk
from tkinter import messagebox, simpledialog
import json

class ToDoApp(ctk.CTk):
    """
    ToDoApp: タスク管理

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
        #制作中、デイリー
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.task_vars = []
        for i, task in enumerate(self.tasks):
            var = ctk.BooleanVar()
            chk = ctk.CTkCheckBox(self.scrollable_frame, text=task, variable=var, width=200)
            chk.pack(anchor="w", padx=10, pady=2)
            chk.bind("<ButtonPress-1>", lambda e, idx=i: self.on_drag(e, idx))
            chk.bind("<B1-Motion>", lambda e: self.on_drag_move(e))
            chk.bind("<ButtonRelease-1>", lambda e: self.on_drop())
            self.task_vars.append(var)
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_drag(self, event, index):
        self.is_dragging = False
        self.dragged_task_index = index
        self.start_x = event.x
        self.start_y = event.y
        self.drag_threshold = 5  # これ以上動いたらドラッグと判定

    def on_drag_move(self, event):
        """ マウスが一定距離以上移動したらドラッグ判定 """
        if self.dragged_task_index is None:
            return

        dx = abs(event.x - self.start_x)
        dy = abs(event.y - self.start_y)
        
        if dx > self.drag_threshold or dy > self.drag_threshold:
            self.is_dragging = True  # ここでドラッグが発生したことを判定

    def on_drop(self):
        """ ドロップ時にドラッグしていたら順番を変更 """
        if self.dragged_task_index is not None and self.is_dragging:
            old_index = self.dragged_task_index
            new_index = len(self.tasks) - 1  # 例として最後に移動
            self.tasks.insert(new_index, self.tasks.pop(old_index))
            self.update_task_list()

        self.dragged_task_index = None
        self.is_dragging = False

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
