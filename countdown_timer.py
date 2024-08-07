import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta

class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("倒计时器")
        
        # 设置窗口总是在最上层
        self.root.attributes("-topmost", True)

        # 设置窗口大小
        self.original_width = 400
        self.original_height = 300
        self.new_height = int(self.original_height * 0.8)  # 减少20%
        self.root.geometry(f"{self.original_width}x{self.new_height}+100+100")

        # 创建标签显示倒计时
        self.label = ttk.Label(self.root, text="00:00:00")
        self.label.pack(pady=10)

        # 创建显示提示信息的标签，字体较小
        self.end_message_label = ttk.Label(self.root, text="", font=("Helvetica", 12))
        self.end_message_label.pack(pady=5)

        # 创建按钮框架
        button_frame1 = ttk.Frame(self.root)
        button_frame1.pack(pady=(10, 5))

        button_frame2 = ttk.Frame(self.root)
        button_frame2.pack(pady=(5, 10))

        # 创建控制倒计时的按钮
        self.start_button = ttk.Button(button_frame1, text="开始", command=self.start_countdown)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = ttk.Button(button_frame1, text="暂停", command=self.pause_countdown)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.set_time_button = ttk.Button(button_frame2, text="设置时长", command=self.ask_for_time)
        self.set_time_button.pack(side=tk.LEFT, padx=5)

        self.restart_button = ttk.Button(button_frame2, text="重新计时", command=self.restart_countdown)
        self.restart_button.pack(side=tk.LEFT, padx=5)

        # 变量存储倒计时时长
        self.countdown_running = False
        self.countdown_paused = False
        self.remaining_time = 0
        self.countdown_time = 0  # 存储倒计时时长

        # 存储上次设置的时长
        self.last_set_hours = ""
        self.last_set_minutes = ""
        self.last_set_seconds = ""

        # 记录倒计时开始时间
        self.start_time = None

        # 初始化倒计时
        self.timer_id = None
        self.pause_time = None

        # 记录初始窗口宽度
        self.initial_width = self.root.winfo_width()

        # 更新字体大小以适应窗口变化
        self.root.bind("<Configure>", self.on_window_resize)

    def on_window_resize(self, event=None):
        # 获取窗口的宽度和高度
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        if width != self.initial_width:
            # 设置字体大小为窗口宽度的15%
            font_size = int(width * 0.15)  # 这里的比例可以根据需求调整

            # 更新标签的字体
            self.label.config(font=("Helvetica", font_size))

            # 更新初始宽度
            self.initial_width = width

    def ask_for_time(self):
        # 创建一个新窗口用于输入时分秒
        self.time_window = tk.Toplevel(self.root)
        self.time_window.title("设置倒计时")

        # 确保对话框在主窗口前面
        self.time_window.attributes("-topmost", True)

        # 设置窗口的大小，80% 宽度比主窗口
        width = int(self.root.winfo_width() * 0.8)
        height = 150  # 可以根据需要调整高度
        self.time_window.geometry(f"{width}x{height}")

        # 设置窗口的布局
        self.time_window.grid_rowconfigure(0, weight=1)
        self.time_window.grid_rowconfigure(1, weight=1)
        self.time_window.grid_rowconfigure(2, weight=1)
        self.time_window.grid_rowconfigure(3, weight=1)
        self.time_window.grid_columnconfigure(0, weight=1)
        self.time_window.grid_columnconfigure(1, weight=1)

        tk.Label(self.time_window, text="时:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(self.time_window, text="分:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Label(self.time_window, text="秒:").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        # 输入框
        self.hours_entry = tk.Entry(self.time_window, width=5)
        self.minutes_entry = tk.Entry(self.time_window, width=5)
        self.seconds_entry = tk.Entry(self.time_window, width=5)
        
        self.hours_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.minutes_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.seconds_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # 填充上次设置的时间
        self.hours_entry.insert(0, self.last_set_hours)
        self.minutes_entry.insert(0, self.last_set_minutes)
        self.seconds_entry.insert(0, self.last_set_seconds)

        # 确认按钮
        ttk.Button(self.time_window, text="确定", command=self.set_countdown_time).grid(row=3, column=0, columnspan=2, pady=10)

    def set_countdown_time(self):
        try:
            # 确保time_window仍然存在
            if not hasattr(self, 'time_window') or not self.time_window.winfo_exists():
                raise RuntimeError("时间设置窗口已关闭或不存在。")

            # 获取用户输入，如果为空则默认为0
            hours = self.hours_entry.get().strip()
            minutes = self.minutes_entry.get().strip()
            seconds = self.seconds_entry.get().strip()

            hours = int(hours) if hours else 0
            minutes = int(minutes) if minutes else 0
            seconds = int(seconds) if seconds else 0

            # 确保输入合法
            if not (0 <= hours <= 23):
                raise ValueError("小时应在0到23之间")
            if not (0 <= minutes <= 59):
                raise ValueError("分钟应在0到59之间")
            if not (0 <= seconds <= 59):
                raise ValueError("秒应在0到59之间")

            # 保存上次设置的时长
            self.last_set_hours = f"{hours:02}"
            self.last_set_minutes = f"{minutes:02}"
            self.last_set_seconds = f"{seconds:02}"

            # 更新倒计时时长
            self.countdown_time = hours * 3600 + minutes * 60 + seconds
            self.remaining_time = self.countdown_time
            
            # 显示设置后的时间
            self.label.config(text=self.format_time(self.remaining_time))
            self.end_message_label.config(text="")

            # 关闭设置窗口
            self.time_window.destroy()
            self.time_window = None  # 清除对话框引用
            self.root.focus()  # 确保主窗口重新获得焦点
        except ValueError as e:
            messagebox.showerror("输入错误", f"请输入有效的数字。错误: {e}")
        except RuntimeError as e:
            messagebox.showerror("错误", str(e))

    def start_countdown(self):
        if self.countdown_time > 0:
            if not self.countdown_running:
                self.countdown_running = True
                if self.countdown_paused:
                    # 从暂停状态恢复
                    self.countdown_paused = False
                    self.update_timer()
                else:
                    # 记录倒计时开始时间
                    self.start_time = datetime.now()
                    self.update_timer()
        else:
            messagebox.showinfo("倒计时未设置", "请设置倒计时时间。")

    def pause_countdown(self):
        if self.countdown_running:
            self.countdown_running = False
            self.countdown_paused = True
            # 记录暂停时的时间
            self.pause_time = self.remaining_time

    def restart_countdown(self):
        if self.countdown_time > 0:
            # 取消现有定时器
            if self.timer_id is not None:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None

            # 使用上一次的倒计时时长
            self.remaining_time = self.countdown_time
            self.countdown_paused = False
            self.countdown_running = True  # 确保重启时立即开始
            self.label.config(text=self.format_time(self.remaining_time))  # 显示重启后的时间
            self.update_timer()  # 直接开始倒计时
        else:
            messagebox.showinfo("倒计时未设置", "请设置倒计时时间。")

    def format_time(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def update_timer(self):
        if self.remaining_time > 0 and self.countdown_running:
            self.label.config(text=self.format_time(self.remaining_time))
            self.remaining_time -= 1
            self.timer_id = self.root.after(1000, self.update_timer)  # 每秒更新一次
        elif self.remaining_time <= 0:
            # 计算倒计时结束的实际时间
            if self.start_time is not None:
                end_time = self.start_time + timedelta(seconds=self.countdown_time)
                end_time_str = end_time.strftime("%H:%M:%S")
            else:
                end_time_str = "未知时间"

            # 更新标签
            self.label.config(text="00:00:00")
            self.end_message_label.config(text=f"{self.format_time(self.countdown_time)} 倒计时结束 结束时间: {end_time_str}")

            # 取消定时器任务
            if self.timer_id is not None:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
            self.countdown_running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()
