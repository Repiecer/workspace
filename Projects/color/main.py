import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
import threading
import queue
import time
from PIL import Image, ImageTk
import random
import os

class VideoSplitColorProcessor:
    """视频分割颜色突显处理器"""
    
    def __init__(self, root):
        # 初始化窗口
        self.root = root
        self.root.title("视频分割颜色突显处理器")
        self.root.geometry("1200x800")
        
        # 状态变量
        self.video_path = None
        self.cap = None
        self.is_playing = False
        self.is_paused = False
        self.current_frame = 0
        self.total_frames = 0
        self.fps = 30
        
        # 分割模式
        self.split_mode = "none"  # none, horizontal, vertical, both
        self.split_modes = {
            "none": "无分割",
            "horizontal": "水平分割",
            "vertical": "垂直分割", 
            "both": "水平和垂直分割"
        }
        
        # 颜色模式
        self.region_colors = {
            "top_left": "red",
            "top_right": "green", 
            "bottom_left": "blue",
            "bottom_right": "random"
        }
        
        # 处理参数
        self.color_sensitivity = 20
        self.min_brightness = 30
        
        # 队列
        self.frame_queue = queue.Queue(maxsize=10)
        self.display_queue = queue.Queue(maxsize=5)
        
        # 性能跟踪
        self.frame_count = 0
        self.start_time = None
        
        # 创建界面
        self.create_widgets()
        
        # 绑定按键
        self.bind_keys()
        
        # 初始化视频显示
        self.init_video_display()
        
        print("程序初始化完成！按 'O' 打开视频文件")
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="视频分割颜色突显处理器", 
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # 控制面板框架
        control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding="10")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 按钮区域
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=0, column=0, sticky=tk.W)
        
        # 控制按钮
        self.open_btn = ttk.Button(button_frame, text="打开视频 (O)", 
                                  command=self.open_video, width=15)
        self.open_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.play_btn = ttk.Button(button_frame, text="播放 (P)", 
                                  command=self.play_video, width=15, state=tk.DISABLED)
        self.play_btn.grid(row=0, column=1, padx=(0, 5))
        
        self.pause_btn = ttk.Button(button_frame, text="暂停 (Space)", 
                                   command=self.pause_video, width=15, state=tk.DISABLED)
        self.pause_btn.grid(row=0, column=2, padx=(0, 5))
        
        self.snapshot_btn = ttk.Button(button_frame, text="截图 (S)", 
                                      command=self.take_snapshot, width=15, state=tk.DISABLED)
        self.snapshot_btn.grid(row=0, column=3, padx=(0, 5))
        
        # 参数调节区域
        param_frame = ttk.Frame(control_frame)
        param_frame.grid(row=0, column=1, sticky=tk.E, padx=(20, 0))
        
        # 颜色敏感度
        ttk.Label(param_frame, text="颜色敏感度:").grid(row=0, column=0, sticky=tk.W)
        self.sensitivity_scale = ttk.Scale(param_frame, from_=0, to=100, 
                                          orient=tk.HORIZONTAL, length=150,
                                          command=self.update_sensitivity)
        self.sensitivity_scale.set(self.color_sensitivity)
        self.sensitivity_scale.grid(row=0, column=1, padx=(5, 10))
        self.sensitivity_label = ttk.Label(param_frame, text=f"{self.color_sensitivity}")
        self.sensitivity_label.grid(row=0, column=2)
        
        # 亮度阈值
        ttk.Label(param_frame, text="亮度阈值:").grid(row=1, column=0, sticky=tk.W)
        self.brightness_scale = ttk.Scale(param_frame, from_=0, to=255, 
                                         orient=tk.HORIZONTAL, length=150,
                                         command=self.update_brightness)
        self.brightness_scale.set(self.min_brightness)
        self.brightness_scale.grid(row=1, column=1, padx=(5, 10))
        self.brightness_label = ttk.Label(param_frame, text=f"{self.min_brightness}")
        self.brightness_label.grid(row=1, column=2)
        
        # 分割模式选择
        mode_frame = ttk.LabelFrame(main_frame, text="分割模式", padding="10")
        mode_frame.grid(row=2, column=0, sticky=(tk.N, tk.S, tk.W), padx=(0, 10))
        
        # 模式按钮
        self.mode_vars = {}
        for i, (mode_key, mode_name) in enumerate(self.split_modes.items()):
            var = tk.BooleanVar()
            self.mode_vars[mode_key] = var
            btn = ttk.Radiobutton(mode_frame, text=mode_name, variable=var,
                                 value=(mode_key == "none"),  # 默认选择none
                                 command=lambda m=mode_key: self.set_split_mode(m))
            btn.grid(row=i, column=0, sticky=tk.W, pady=2)
            if mode_key == "none":
                btn.invoke()  # 选择默认模式
        
        # 区域颜色设置
        color_frame = ttk.LabelFrame(main_frame, text="区域颜色设置", padding="10")
        color_frame.grid(row=2, column=1, sticky=(tk.N, tk.S, tk.W, tk.E), padx=(0, 10))
        
        # 颜色选择下拉框
        color_options = ["red", "green", "blue", "random", "custom"]
        self.color_vars = {}
        
        for i, region in enumerate(self.region_colors.keys()):
            ttk.Label(color_frame, text=f"{region.replace('_', ' ').title()}:").grid(
                row=i, column=0, sticky=tk.W, pady=2)
            
            var = tk.StringVar(value=self.region_colors[region])
            self.color_vars[region] = var
            
            combo = ttk.Combobox(color_frame, textvariable=var, 
                                values=color_options, state="readonly", width=12)
            combo.grid(row=i, column=1, padx=(5, 0), pady=2)
            combo.bind("<<ComboboxSelected>>", lambda e, r=region: self.update_region_color(r))
        
        # 自定义颜色设置
        ttk.Label(color_frame, text="自定义颜色 (B,G,R):").grid(row=4, column=0, sticky=tk.W, pady=(10, 2))
        self.custom_color_entry = ttk.Entry(color_frame, width=15)
        self.custom_color_entry.grid(row=4, column=1, padx=(5, 0), pady=(10, 2))
        self.custom_color_entry.insert(0, "0,0,255")
        
        # 视频显示区域
        self.video_frame = ttk.LabelFrame(main_frame, text="视频预览", padding="10")
        self.video_frame.grid(row=2, column=2, sticky=(tk.N, tk.S, tk.W, tk.E))
        
        # 创建Canvas用于显示视频
        self.canvas = tk.Canvas(self.video_frame, bg="black", width=640, height=480)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 状态栏
        self.status_bar = ttk.Label(main_frame, text="就绪", relief=tk.SUNKEN)
        self.status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 信息显示标签
        self.info_label = ttk.Label(main_frame, text="", font=("Arial", 10))
        self.info_label.grid(row=4, column=0, columnspan=3, pady=(5, 0))
    
    def bind_keys(self):
        """绑定键盘快捷键"""
        self.root.bind('o', lambda e: self.open_video())
        self.root.bind('O', lambda e: self.open_video())
        self.root.bind('p', lambda e: self.play_video())
        self.root.bind('P', lambda e: self.play_video())
        self.root.bind('<space>', lambda e: self.pause_video())
        self.root.bind('s', lambda e: self.take_snapshot())
        self.root.bind('S', lambda e: self.take_snapshot())
        
        # 分割模式快捷键
        self.root.bind('1', lambda e: self.set_split_mode("none"))
        self.root.bind('2', lambda e: self.set_split_mode("horizontal"))
        self.root.bind('3', lambda e: self.set_split_mode("vertical"))
        self.root.bind('4', lambda e: self.set_split_mode("both"))
        
        # 随机颜色快捷键
        self.root.bind('r', lambda e: self.randomize_colors())
        self.root.bind('R', lambda e: self.randomize_colors())
        
        # 退出快捷键
        self.root.bind('<Escape>', lambda e: self.root.quit())
    
    def init_video_display(self):
        """初始化视频显示"""
        # 创建初始黑色图像
        blank_image = np.zeros((480, 640, 3), dtype=np.uint8)
        self.update_display(blank_image)
    
    def open_video(self):
        """打开视频文件"""
        file_path = filedialog.askopenfilename(
            title="选择视频文件",
            filetypes=[
                ("视频文件", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv"),
                ("所有文件", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        # 释放之前的视频
        if self.cap is not None:
            self.cap.release()
        
        # 尝试打开视频
        try:
            self.cap = cv2.VideoCapture(file_path)
            if not self.cap.isOpened():
                raise Exception("无法打开视频文件")
            
            self.video_path = file_path
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            if self.fps == 0:
                self.fps = 30
            
            # 启用播放按钮
            self.play_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.NORMAL)
            self.snapshot_btn.config(state=tk.NORMAL)
            
            # 显示视频信息
            filename = os.path.basename(file_path)
            self.status_bar.config(text=f"已打开: {filename} | 总帧数: {self.total_frames} | FPS: {self.fps}")
            
            # 显示第一帧
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = 1
                processed_frame = self.process_frame(frame)
                self.update_display(processed_frame)
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 重置到第一帧
            
        except Exception as e:
            messagebox.showerror("错误", f"无法打开视频文件: {str(e)}")
    
    def play_video(self):
        """播放视频"""
        if self.cap is None or not self.cap.isOpened():
            messagebox.showwarning("警告", "请先打开视频文件")
            return
        
        if self.is_playing:
            return
        
        self.is_playing = True
        self.is_paused = False
        self.start_time = time.time()
        self.frame_count = 0
        
        # 启动处理线程
        self.processing_thread = threading.Thread(target=self.video_processing_loop, daemon=True)
        self.processing_thread.start()
        
        # 启动显示更新
        self.update_video_display()
        
        self.status_bar.config(text="播放中...")
    
    def pause_video(self):
        """暂停/继续视频"""
        if not self.is_playing:
            return
        
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.status_bar.config(text="已暂停")
        else:
            self.status_bar.config(text="播放中...")
    
    def set_split_mode(self, mode):
        """设置分割模式"""
        self.split_mode = mode
        
        # 更新单选按钮状态
        for mode_key, var in self.mode_vars.items():
            var.set(mode_key == mode)
        
        self.status_bar.config(text=f"分割模式: {self.split_modes[mode]}")
    
    def update_sensitivity(self, value):
        """更新颜色敏感度"""
        self.color_sensitivity = int(float(value))
        self.sensitivity_label.config(text=f"{self.color_sensitivity}")
    
    def update_brightness(self, value):
        """更新亮度阈值"""
        self.min_brightness = int(float(value))
        self.brightness_label.config(text=f"{self.min_brightness}")
    
    def update_region_color(self, region):
        """更新区域颜色"""
        color = self.color_vars[region].get()
        self.region_colors[region] = color
        print(f"区域 {region} 颜色更新为: {color}")
    
    def randomize_colors(self):
        """随机化所有区域颜色"""
        colors = ["red", "green", "blue", "random"]
        for region in self.region_colors.keys():
            color = random.choice(colors)
            self.region_colors[region] = color
            self.color_vars[region].set(color)
        
        self.status_bar.config(text="颜色已随机化")
        print("所有区域颜色已随机化")
    
    def get_color_mask(self, frame, color_mode):
        """获取颜色掩码"""
        b, g, r = cv2.split(frame)
        
        if color_mode == "red":
            mask = (r > g + self.color_sensitivity) & (r > b + self.color_sensitivity)
        elif color_mode == "green":
            mask = (g > r + self.color_sensitivity) & (g > b + self.color_sensitivity)
        elif color_mode == "blue":
            mask = (b > r + self.color_sensitivity) & (b > g + self.color_sensitivity)
        elif color_mode == "random":
            # 随机选择一种颜色
            colors = ["red", "green", "blue"]
            color = random.choice(colors)
            return self.get_color_mask(frame, color)
        elif color_mode == "custom":
            # 自定义颜色
            try:
                b_val, g_val, r_val = map(int, self.custom_color_entry.get().split(','))
                color_diff = np.sqrt(
                    (b.astype(float) - b_val) ** 2 +
                    (g.astype(float) - g_val) ** 2 +
                    (r.astype(float) - r_val) ** 2
                )
                mask = color_diff < self.color_sensitivity
            except:
                mask = np.ones(frame.shape[:2], dtype=bool)
        else:
            mask = np.ones(frame.shape[:2], dtype=bool)
        
        # 应用亮度阈值
        brightness = 0.299 * r + 0.587 * g + 0.114 * b
        mask = mask & (brightness > self.min_brightness)
        
        return mask
    
    def process_frame(self, frame):
        """处理单帧图像"""
        height, width = frame.shape[:2]
        result = np.zeros_like(frame)
        
        # 根据分割模式处理
        if self.split_mode == "none":
            # 无分割，整个画面使用左上区域的颜色
            color_mode = self.region_colors["top_left"]
            mask = self.get_color_mask(frame, color_mode)
            
            # 计算灰度值
            b, g, r = cv2.split(frame)
            gray_values = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)
            
            # 应用处理
            result[mask] = frame[mask]
            non_mask = ~mask
            result[non_mask, 0] = gray_values[non_mask]
            result[non_mask, 1] = gray_values[non_mask]
            result[non_mask, 2] = gray_values[non_mask]
            
            # 绘制分割线（不分割但显示区域）
            cv2.line(result, (0, height//2), (width, height//2), (255, 255, 255), 1)
            cv2.line(result, (width//2, 0), (width//2, height), (255, 255, 255), 1)
            
        elif self.split_mode == "horizontal":
            # 水平分割
            top_half = frame[0:height//2, :]
            bottom_half = frame[height//2:, :]
            
            # 处理上半部分（使用左上颜色）
            top_result = self.apply_color_filter(top_half, self.region_colors["top_left"])
            result[0:height//2, :] = top_result
            
            # 处理下半部分（使用左下颜色）
            bottom_result = self.apply_color_filter(bottom_half, self.region_colors["bottom_left"])
            result[height//2:, :] = bottom_result
            
            # 绘制分割线
            cv2.line(result, (0, height//2), (width, height//2), (0, 255, 255), 3)
            
        elif self.split_mode == "vertical":
            # 垂直分割
            left_half = frame[:, 0:width//2]
            right_half = frame[:, width//2:]
            
            # 处理左半部分（使用左上颜色）
            left_result = self.apply_color_filter(left_half, self.region_colors["top_left"])
            result[:, 0:width//2] = left_result
            
            # 处理右半部分（使用右上颜色）
            right_result = self.apply_color_filter(right_half, self.region_colors["top_right"])
            result[:, width//2:] = right_result
            
            # 绘制分割线
            cv2.line(result, (width//2, 0), (width//2, height), (0, 255, 255), 3)
            
        elif self.split_mode == "both":
            # 水平和垂直分割（四等分）
            half_h = height // 2
            half_w = width // 2
            
            # 四个区域
            top_left = frame[0:half_h, 0:half_w]
            top_right = frame[0:half_h, half_w:]
            bottom_left = frame[half_h:, 0:half_w]
            bottom_right = frame[half_h:, half_w:]
            
            # 分别处理每个区域
            tl_result = self.apply_color_filter(top_left, self.region_colors["top_left"])
            tr_result = self.apply_color_filter(top_right, self.region_colors["top_right"])
            bl_result = self.apply_color_filter(bottom_left, self.region_colors["bottom_left"])
            br_result = self.apply_color_filter(bottom_right, self.region_colors["bottom_right"])
            
            # 合并结果
            result[0:half_h, 0:half_w] = tl_result
            result[0:half_h, half_w:] = tr_result
            result[half_h:, 0:half_w] = bl_result
            result[half_h:, half_w:] = br_result
            
            # 绘制分割线
            cv2.line(result, (0, half_h), (width, half_h), (0, 255, 255), 3)
            cv2.line(result, (half_w, 0), (half_w, height), (0, 255, 255), 3)
        
        return result
    
    def apply_color_filter(self, region_frame, color_mode):
        """对区域应用颜色滤镜"""
        height, width = region_frame.shape[:2]
        result = np.zeros_like(region_frame)
        
        # 获取颜色掩码
        mask = self.get_color_mask(region_frame, color_mode)
        
        # 计算灰度值
        b, g, r = cv2.split(region_frame)
        gray_values = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)
        
        # 应用处理
        result[mask] = region_frame[mask]
        non_mask = ~mask
        result[non_mask, 0] = gray_values[non_mask]
        result[non_mask, 1] = gray_values[non_mask]
        result[non_mask, 2] = gray_values[non_mask]
        
        return result
    
    def video_processing_loop(self):
        """视频处理循环"""
        while self.is_playing and self.cap is not None:
            if self.is_paused:
                time.sleep(0.1)
                continue
            
            # 读取帧
            ret, frame = self.cap.read()
            if not ret:
                # 视频结束，重置到开头
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            
            # 处理帧
            processed_frame = self.process_frame(frame)
            
            # 放入队列
            try:
                self.frame_queue.put((frame, processed_frame), timeout=0.5)
            except queue.Full:
                pass  # 队列满时跳过
            
            self.current_frame += 1
            self.frame_count += 1
            
            # 控制帧率
            time.sleep(1.0 / self.fps)
    
    def update_video_display(self):
        """更新视频显示"""
        if not self.is_playing:
            return
        
        try:
            # 从队列获取帧
            original, processed = self.frame_queue.get(timeout=0.1)
            
            # 更新显示
            self.update_display(processed)
            
            # 更新信息
            elapsed = time.time() - self.start_time
            fps = self.frame_count / elapsed if elapsed > 0 else 0
            
            info_text = (f"帧: {self.current_frame}/{self.total_frames} | "
                        f"FPS: {fps:.1f} | "
                        f"模式: {self.split_modes[self.split_mode]} | "
                        f"敏感度: {self.color_sensitivity}")
            self.info_label.config(text=info_text)
            
        except queue.Empty:
            pass  # 队列为空，跳过
        
        # 继续更新
        self.root.after(10, self.update_video_display)
    
    def update_display(self, frame):
        """更新显示画面"""
        # 调整大小以适应Canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:
            # 计算缩放比例
            frame_height, frame_width = frame.shape[:2]
            scale_w = canvas_width / frame_width
            scale_h = canvas_height / frame_height
            scale = min(scale_w, scale_h)
            
            new_width = int(frame_width * scale)
            new_height = int(frame_height * scale)
            
            if new_width > 0 and new_height > 0:
                frame_resized = cv2.resize(frame, (new_width, new_height))
            else:
                frame_resized = frame
        else:
            frame_resized = cv2.resize(frame, (640, 480))
        
        # 转换为PIL图像
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)
        
        # 转换为Tkinter图像
        self.tk_image = ImageTk.PhotoImage(pil_image)
        
        # 更新Canvas
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width//2, canvas_height//2, 
                                anchor=tk.CENTER, image=self.tk_image)
    
    def take_snapshot(self):
        """截图保存"""
        if not self.is_playing:
            messagebox.showwarning("警告", "请先播放视频")
            return
        
        try:
            # 从队列获取当前帧
            original, processed = self.frame_queue.get(timeout=0.5)
            
            # 保存文件
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            
            # 创建保存目录
            save_dir = "snapshots"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            # 保存原始帧
            original_path = os.path.join(save_dir, f"original_{timestamp}.jpg")
            cv2.imwrite(original_path, original)
            
            # 保存处理后的帧
            processed_path = os.path.join(save_dir, f"processed_{timestamp}.jpg")
            cv2.imwrite(processed_path, processed)
            
            # 保存并排对比
            combined = np.hstack([original, processed])
            combined_path = os.path.join(save_dir, f"combined_{timestamp}.jpg")
            cv2.imwrite(combined_path, combined)
            
            self.status_bar.config(text=f"截图已保存到 {save_dir} 目录")
            print(f"截图已保存: {original_path}, {processed_path}, {combined_path}")
            
        except Exception as e:
            messagebox.showerror("错误", f"截图失败: {str(e)}")
    
    def on_closing(self):
        """关闭窗口时的清理"""
        self.is_playing = False
        
        if self.cap is not None:
            self.cap.release()
        
        self.root.destroy()

# 主程序
def main():
    """主程序入口"""
    root = tk.Tk()
    
    # 创建应用程序
    app = VideoSplitColorProcessor(root)
    
    # 设置关闭事件处理
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    print("启动视频分割颜色突显处理器...")
    print("=" * 60)
    print("快捷键说明:")
    print("  O - 打开视频文件")
    print("  P - 播放视频")
    print("  Space - 暂停/继续")
    print("  S - 截图保存")
    print("  1 - 无分割模式")
    print("  2 - 水平分割模式")
    print("  3 - 垂直分割模式")
    print("  4 - 水平和垂直分割")
    print("  R - 随机化区域颜色")
    print("  ESC - 退出程序")
    print("=" * 60)
    
    main()