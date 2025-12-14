import cv2
import numpy as np
import time
from datetime import datetime
import threading
import queue
import sys

class ColorHighlightVideoProcessor:
    """多功能颜色突显视频处理器"""
    
    def __init__(self):
        """初始化"""
        # 处理模式
        self.mode = "red"  # 默认突显红色
        self.modes = {
            "red": "突显红色",
            "green": "突显绿色", 
            "blue": "突显蓝色",
            "custom": "自定义颜色",
            "complement": "互补色",
            "dual": "红蓝双色",
            "warm": "暖色系",
            "cool": "冷色系"
        }
        
        # 处理参数
        self.color_sensitivity = 20  # 颜色敏感度
        self.min_brightness = 30     # 最小亮度阈值
        
        # 视频相关
        self.video_source = None     # 视频源
        self.cap = None              # 视频捕获对象
        self.output_writer = None    # 视频写入对象
        self.is_recording = False    # 是否正在录制
        self.recording_path = None   # 录制保存路径
        
        # 状态信息
        self.is_playing = False
        self.current_frame = 0
        self.total_frames = 0
        self.fps = 0
        self.frame_queue = queue.Queue(maxsize=30)
        self.display_queue = queue.Queue(maxsize=10)
        
        # 性能跟踪
        self.processing_times = []
        self.frame_count = 0
        self.start_time = None
        
        # 自定义颜色 (B, G, R)
        self.custom_color = (255, 0, 0)  # 默认蓝色
        
        # 显示设置
        self.display_mode = "side_by_side"  # side_by_side, split_screen, processed_only, original_only
        self.show_info = True
        self.show_mask = False
        
    def initialize_video_source(self, source):
        """初始化视频源"""
        self.video_source = source
        
        if source.isdigit():  # 摄像头ID
            source_id = int(source)
            self.cap = cv2.VideoCapture(source_id)
            print(f"打开摄像头 {source_id}")
        else:  # 视频文件
            self.cap = cv2.VideoCapture(source)
            print(f"打开视频文件: {source}")
        
        if not self.cap.isOpened():
            print(f"错误：无法打开视频源 {source}")
            return False
        
        # 获取视频属性
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        if self.fps == 0:  # 摄像头可能返回0
            self.fps = 30
        
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"视频信息: {self.width}x{self.height}, {self.fps}FPS")
        if self.total_frames > 0:
            print(f"总帧数: {self.total_frames}")
        
        return True
    
    def get_color_mask(self, frame, target_color):
        """
        获取颜色掩码
        
        参数:
        - frame: 输入帧 (BGR格式)
        - target_color: 目标颜色 ('red', 'green', 'blue', 'custom')
        
        返回:
        - 颜色掩码 (True表示匹配目标颜色)
        """
        b, g, r = cv2.split(frame)
        
        if target_color == "red":
            # 红色突出: R > G + sensitivity 且 R > B + sensitivity
            mask = (r > g + self.color_sensitivity) & (r > b + self.color_sensitivity)
            
        elif target_color == "green":
            # 绿色突出: G > R + sensitivity 且 G > B + sensitivity
            mask = (g > r + self.color_sensitivity) & (g > b + self.color_sensitivity)
            
        elif target_color == "blue":
            # 蓝色突出: B > R + sensitivity 且 B > G + sensitivity
            mask = (b > r + self.color_sensitivity) & (b > g + self.color_sensitivity)
            
        elif target_color == "custom":
            # 自定义颜色
            target_b, target_g, target_r = self.custom_color
            # 计算颜色距离
            color_diff = np.sqrt(
                (b.astype(float) - target_b) ** 2 +
                (g.astype(float) - target_g) ** 2 +
                (r.astype(float) - target_r) ** 2
            )
            mask = color_diff < self.color_sensitivity
            
        elif target_color == "complement":
            # 互补色模式：保留目标颜色，其他转为互补色
            # 这里简化为保留暖色调
            mask = (r > 150) & (g > 100) & (b < 100)
            
        elif target_color == "dual":
            # 双色模式：突出红色和蓝色
            mask_red = (r > g + self.color_sensitivity) & (r > b + self.color_sensitivity)
            mask_blue = (b > r + self.color_sensitivity) & (b > g + self.color_sensitivity)
            mask = mask_red | mask_blue
            
        elif target_color == "warm":
            # 暖色系：红色和黄色
            mask_red = (r > g + self.color_sensitivity) & (r > b + self.color_sensitivity)
            mask_yellow = (r > 150) & (g > 150) & (b < 100)
            mask = mask_red | mask_yellow
            
        elif target_color == "cool":
            # 冷色系：蓝色和青色
            mask_blue = (b > r + self.color_sensitivity) & (b > g + self.color_sensitivity)
            mask_cyan = (g > 150) & (b > 150) & (r < 100)
            mask = mask_blue | mask_cyan
            
        else:
            mask = np.ones(frame.shape[:2], dtype=bool)
        
        # 应用亮度阈值
        brightness = 0.299 * r + 0.587 * g + 0.114 * b
        mask = mask & (brightness > self.min_brightness)
        
        return mask
    
    def process_frame(self, frame):
        """处理单帧图像"""
        start_time = time.time()
        
        # 获取原始帧的副本
        original = frame.copy()
        
        # 获取颜色掩码
        color_mask = self.get_color_mask(frame, self.mode)
        
        # 计算灰度值
        b, g, r = cv2.split(frame)
        gray_values = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)
        
        # 创建结果图像
        result = np.zeros_like(frame)
        
        # 保留目标颜色的像素
        result[color_mask] = frame[color_mask]
        
        # 其他像素转为黑白
        non_color_mask = ~color_mask
        if np.any(non_color_mask):
            result[non_color_mask, 0] = gray_values[non_color_mask]
            result[non_color_mask, 1] = gray_values[non_color_mask]
            result[non_color_mask, 2] = gray_values[non_color_mask]
        
        # 记录处理时间
        process_time = time.time() - start_time
        self.processing_times.append(process_time)
        if len(self.processing_times) > 100:
            self.processing_times.pop(0)
        
        # 计算颜色像素比例
        color_pct = np.sum(color_mask) / (frame.shape[0] * frame.shape[1]) * 100
        
        return original, result, color_mask, color_pct, process_time
    
    def create_display_frame(self, original, processed, color_mask, info):
        """创建显示帧"""
        # 根据显示模式组合图像
        if self.display_mode == "side_by_side":
            display = np.hstack([original, processed])
            
        elif self.display_mode == "split_screen":
            # 上下分割
            display = np.vstack([original, processed])
            
        elif self.display_mode == "processed_only":
            display = processed.copy()
            
        elif self.display_mode == "original_only":
            display = original.copy()
            
        elif self.display_mode == "quad_view":
            # 四视图：原图、处理图、掩码、统计
            mask_display = (color_mask * 255).astype(np.uint8)
            mask_display = cv2.cvtColor(mask_display, cv2.COLOR_GRAY2BGR)
            
            # 创建统计图（简单版本）
            stats_img = np.zeros((self.height // 2, self.width // 2, 3), dtype=np.uint8)
            cv2.putText(stats_img, f"Mode: {self.mode}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.putText(stats_img, f"Color %: {info['color_pct']:.1f}%", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.putText(stats_img, f"Process: {info['process_time']*1000:.1f}ms", (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            # 调整大小
            resized_orig = cv2.resize(original, (self.width // 2, self.height // 2))
            resized_proc = cv2.resize(processed, (self.width // 2, self.height // 2))
            resized_mask = cv2.resize(mask_display, (self.width // 2, self.height // 2))
            
            # 组合四视图
            top_row = np.hstack([resized_orig, resized_proc])
            bottom_row = np.hstack([resized_mask, stats_img])
            display = np.vstack([top_row, bottom_row])
            
        else:
            display = np.hstack([original, processed])
        
        # 添加信息覆盖层
        if self.show_info:
            display = self.add_info_overlay(display, info)
        
        return display
    
    def add_info_overlay(self, frame, info):
        """添加信息覆盖层"""
        overlay = frame.copy()
        
        # 添加边框
        cv2.rectangle(overlay, (5, 5), (frame.shape[1] - 5, frame.shape[0] - 5), 
                     (0, 0, 0), 2)
        
        # 模式信息
        mode_text = f"Mode: {self.modes.get(self.mode, self.mode)}"
        cv2.putText(overlay, mode_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # 统计信息
        stats_y = 60
        cv2.putText(overlay, f"Frame: {self.current_frame}/{self.total_frames}", 
                   (10, stats_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        if self.total_frames > 0:
            progress = self.current_frame / self.total_frames * 100
            cv2.putText(overlay, f"Progress: {progress:.1f}%", 
                       (10, stats_y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        cv2.putText(overlay, f"Color Pixels: {info['color_pct']:.1f}%", 
                   (10, stats_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        avg_time = np.mean(self.processing_times) if self.processing_times else 0
        cv2.putText(overlay, f"Process Time: {avg_time*1000:.1f}ms", 
                   (10, stats_y + 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # 录制状态
        if self.is_recording:
            cv2.putText(overlay, "RECORDING", (frame.shape[1] - 150, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.putText(overlay, "●", (frame.shape[1] - 180, 35),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), -1)
        
        # 帮助提示
        help_y = frame.shape[0] - 20
        help_text = "R/G/B:颜色模式  +/-:敏感度  D:显示模式  S:保存帧  V:录制  Q:退出"
        cv2.putText(overlay, help_text, (10, help_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        # 当前参数
        param_text = f"Sensitivity: {self.color_sensitivity}  Min Bright: {self.min_brightness}"
        cv2.putText(overlay, param_text, (frame.shape[1] - 300, help_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        return overlay
    
    def start_recording(self, output_path):
        """开始录制视频"""
        if self.is_recording:
            print("已经在录制中")
            return False
        
        # 设置视频编码
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 或 'XVID', 'H264'
        
        # 确定输出尺寸
        if self.display_mode == "side_by_side":
            output_width = self.width * 2
            output_height = self.height
        elif self.display_mode == "split_screen":
            output_width = self.width
            output_height = self.height * 2
        elif self.display_mode == "quad_view":
            output_width = self.width
            output_height = self.height
        else:
            output_width = self.width
            output_height = self.height
        
        # 创建VideoWriter
        self.output_writer = cv2.VideoWriter(
            output_path, fourcc, self.fps, (output_width, output_height)
        )
        
        if not self.output_writer.isOpened():
            print(f"错误：无法创建输出视频文件 {output_path}")
            return False
        
        self.is_recording = True
        self.recording_path = output_path
        print(f"开始录制: {output_path}")
        
        return True
    
    def stop_recording(self):
        """停止录制"""
        if self.is_recording and self.output_writer:
            self.output_writer.release()
            self.is_recording = False
            print(f"录制已停止，保存到: {self.recording_path}")
            return True
        return False
    
    def processing_thread(self):
        """处理线程"""
        while self.is_playing:
            try:
                # 从队列获取帧
                frame = self.frame_queue.get(timeout=1)
                
                # 处理帧
                original, processed, color_mask, color_pct, process_time = self.process_frame(frame)
                
                # 准备信息
                info = {
                    'color_pct': color_pct,
                    'process_time': process_time
                }
                
                # 创建显示帧
                display_frame = self.create_display_frame(original, processed, color_mask, info)
                
                # 如果正在录制，写入视频
                if self.is_recording and self.output_writer:
                    self.output_writer.write(display_frame)
                
                # 放入显示队列
                self.display_queue.put((display_frame, original, processed))
                
                # 更新帧计数
                self.current_frame += 1
                self.frame_count += 1
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"处理线程错误: {e}")
                break
    
    def run(self):
        """主运行函数"""
        # 获取视频源
        print("请选择视频源:")
        print("  0: 默认摄像头")
        print("  1: 第二个摄像头")
        print("  或输入视频文件路径")
        
        source = input("请输入: ").strip()
        if not source:
            source = "0"
        
        if not self.initialize_video_source(source):
            print("无法初始化视频源，程序退出")
            return
        
        self.is_playing = True
        self.start_time = time.time()
        
        # 启动处理线程
        process_thread = threading.Thread(target=self.processing_thread)
        process_thread.daemon = True
        process_thread.start()
        
        print("\n" + "="*60)
        print("多功能颜色突显视频处理器")
        print("="*60)
        print("控制按键:")
        print("  R / G / B - 突显红色/绿色/蓝色")
        print("  1-8       - 选择处理模式")
        print("  +/-       - 增加/减少颜色敏感度")
        print("  [ / ]     - 增加/减少亮度阈值")
        print("  D         - 切换显示模式")
        print("  M         - 显示/隐藏掩码")
        print("  I         - 显示/隐藏信息")
        print("  S         - 保存当前帧")
        print("  V         - 开始/停止录制视频")
        print("  Space     - 暂停/继续播放")
        print("  Q / ESC   - 退出程序")
        print("="*60)
        
        # 主显示循环
        last_key_time = time.time()
        pause_state = False
        
        while self.is_playing:
            if not pause_state:
                # 读取新帧
                ret, frame = self.cap.read()
                if not ret:
                    if self.video_source.isdigit():  # 摄像头
                        continue
                    else:  # 视频文件结束
                        print("视频播放结束")
                        break
                
                # 放入处理队列
                try:
                    self.frame_queue.put(frame, timeout=0.5)
                except queue.Full:
                    pass  # 队列满时跳过帧
            
            # 从显示队列获取结果
            try:
                display_frame, original, processed = self.display_queue.get(timeout=0.1)
                
                # 显示结果
                cv2.imshow('Color Highlight Video Processor', display_frame)
                
                # 计算并显示实时FPS
                elapsed = time.time() - self.start_time
                if elapsed > 0:
                    current_fps = self.frame_count / elapsed
                    if self.frame_count % 30 == 0:
                        print(f"实时FPS: {current_fps:.1f}, 处理模式: {self.mode}", end='\r')
                
            except queue.Empty:
                # 显示队列为空，显示等待信息
                if not pause_state:
                    wait_img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                    cv2.putText(wait_img, "Processing...", (self.width//2-100, self.height//2),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.imshow('Color Highlight Video Processor', wait_img)
            
            # 处理键盘输入
            key = cv2.waitKey(1) & 0xFF
            
            if key != 255 and time.time() - last_key_time > 0.2:  # 防按键抖动
                last_key_time = time.time()
                
                # 颜色模式选择
                if key == ord('r'):
                    self.mode = "red"
                    print(f"切换到: {self.modes['red']}")
                    
                elif key == ord('g'):
                    self.mode = "green"
                    print(f"切换到: {self.modes['green']}")
                    
                elif key == ord('b'):
                    self.mode = "blue"
                    print(f"切换到: {self.modes['blue']}")
                
                # 数字键选择模式
                elif key == ord('1'):
                    self.mode = "red"
                    print(f"切换到: {self.modes['red']}")
                elif key == ord('2'):
                    self.mode = "green"
                    print(f"切换到: {self.modes['green']}")
                elif key == ord('3'):
                    self.mode = "blue"
                    print(f"切换到: {self.modes['blue']}")
                elif key == ord('4'):
                    self.mode = "custom"
                    print(f"切换到: {self.modes['custom']}")
                elif key == ord('5'):
                    self.mode = "complement"
                    print(f"切换到: {self.modes['complement']}")
                elif key == ord('6'):
                    self.mode = "dual"
                    print(f"切换到: {self.modes['dual']}")
                elif key == ord('7'):
                    self.mode = "warm"
                    print(f"切换到: {self.modes['warm']}")
                elif key == ord('8'):
                    self.mode = "cool"
                    print(f"切换到: {self.modes['cool']}")
                
                # 参数调整
                elif key == ord('+') or key == ord('='):
                    self.color_sensitivity = min(self.color_sensitivity + 5, 100)
                    print(f"颜色敏感度: {self.color_sensitivity}")
                    
                elif key == ord('-') or key == ord('_'):
                    self.color_sensitivity = max(self.color_sensitivity - 5, 0)
                    print(f"颜色敏感度: {self.color_sensitivity}")
                    
                elif key == ord('['):
                    self.min_brightness = max(self.min_brightness - 10, 0)
                    print(f"亮度阈值: {self.min_brightness}")
                    
                elif key == ord(']'):
                    self.min_brightness = min(self.min_brightness + 10, 255)
                    print(f"亮度阈值: {self.min_brightness}")
                
                # 显示控制
                elif key == ord('d'):
                    modes = ["side_by_side", "split_screen", "processed_only", "original_only", "quad_view"]
                    current_idx = modes.index(self.display_mode) if self.display_mode in modes else 0
                    self.display_mode = modes[(current_idx + 1) % len(modes)]
                    print(f"显示模式: {self.display_mode}")
                    
                elif key == ord('m'):
                    self.show_mask = not self.show_mask
                    print(f"显示掩码: {'开' if self.show_mask else '关'}")
                    
                elif key == ord('i'):
                    self.show_info = not self.show_info
                    print(f"显示信息: {'开' if self.show_info else '关'}")
                
                # 保存功能
                elif key == ord('s'):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    try:
                        display_frame, original, processed = self.display_queue.get(timeout=0.5)
                        cv2.imwrite(f"snapshot_original_{timestamp}.jpg", original)
                        cv2.imwrite(f"snapshot_processed_{timestamp}.jpg", processed)
                        cv2.imwrite(f"snapshot_display_{timestamp}.jpg", display_frame)
                        print(f"截图已保存: snapshot_*_{timestamp}.jpg")
                    except queue.Empty:
                        print("无法获取当前帧进行保存")
                
                # 录制控制
                elif key == ord('v'):
                    if not self.is_recording:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_path = f"recording_{timestamp}.mp4"
                        if self.start_recording(output_path):
                            print(f"开始录制: {output_path}")
                        else:
                            print("开始录制失败")
                    else:
                        if self.stop_recording():
                            print("录制已停止")
                        else:
                            print("停止录制失败")
                
                # 播放控制
                elif key == 32:  # 空格键
                    pause_state = not pause_state
                    print(f"播放: {'暂停' if pause_state else '继续'}")
                    
                elif key == ord('q') or key == 27:  # Q 或 ESC
                    print("正在退出...")
                    self.is_playing = False
                    break
                
                elif key == ord('c'):
                    # 自定义颜色选择
                    print("自定义颜色选择 (B G R 格式):")
                    try:
                        color_input = input("输入三个0-255的数字 (如: 0 0 255 表示红色): ")
                        b, g, r = map(int, color_input.split())
                        if 0 <= b <= 255 and 0 <= g <= 255 and 0 <= r <= 255:
                            self.custom_color = (b, g, r)
                            self.mode = "custom"
                            print(f"自定义颜色设置为: B={b}, G={g}, R={r}")
                        else:
                            print("颜色值必须在0-255范围内")
                    except:
                        print("输入格式错误，使用默认值")
        
        # 清理资源
        self.cleanup()
        
    def cleanup(self):
        """清理资源"""
        self.is_playing = False
        
        # 停止录制
        if self.is_recording:
            self.stop_recording()
        
        # 释放视频资源
        if self.cap:
            self.cap.release()
        
        # 关闭所有窗口
        cv2.destroyAllWindows()
        
        # 输出统计信息
        total_time = time.time() - self.start_time if self.start_time else 0
        print("\n" + "="*60)
        print("处理统计:")
        print(f"总处理帧数: {self.frame_count}")
        print(f"总时间: {total_time:.1f}秒")
        if total_time > 0:
            print(f"平均FPS: {self.frame_count/total_time:.1f}")
        
        if self.processing_times:
            avg_process = np.mean(self.processing_times) * 1000
            max_process = np.max(self.processing_times) * 1000
            print(f"平均处理时间: {avg_process:.1f}ms")
            print(f"最大处理时间: {max_process:.1f}ms")
        
        print("程序结束")
        print("="*60)

# 简化版本（快速测试）
def quick_start():
    """快速启动简化版本"""
    print("快速启动颜色突显视频处理器...")
    
    processor = ColorHighlightVideoProcessor()
    
    # 使用默认摄像头
    if processor.initialize_video_source("0"):
        processor.run()
    else:
        print("无法打开摄像头")

# 处理视频文件版本
def process_video_file(video_path):
    """处理指定视频文件"""
    print(f"处理视频文件: {video_path}")
    
    processor = ColorHighlightVideoProcessor()
    
    if processor.initialize_video_source(video_path):
        processor.run()
    else:
        print(f"无法打开视频文件: {video_path}")

# 命令行界面
def main():
    """主程序入口"""
    print("=" * 70)
    print("多功能颜色突显视频处理器")
    print("=" * 70)
    print("功能说明:")
    print("- 实时突显指定颜色的像素，其他像素转为黑白")
    print("- 支持多种颜色模式：红、绿、蓝、自定义等")
    print("- 支持实时摄像头和视频文件处理")
    print("- 可调节颜色敏感度和亮度阈值")
    print("- 支持视频录制和截图保存")
    print()
    
    while True:
        print("请选择操作:")
        print("1. 快速启动（默认摄像头）")
        print("2. 处理视频文件")
        print("3. 选择摄像头ID")
        print("4. 退出")
        
        choice = input("请输入选择 (1-4): ").strip()
        
        if choice == '1':
            print("\n启动快速版本...")
            quick_start()
            
        elif choice == '2':
            video_path = input("请输入视频文件路径: ").strip()
            if video_path:
                process_video_file(video_path)
            else:
                print("请输入有效的文件路径")
                
        elif choice == '3':
            cam_id = input("请输入摄像头ID (默认0): ").strip()
            cam_id = cam_id if cam_id else "0"
            
            processor = ColorHighlightVideoProcessor()
            if processor.initialize_video_source(cam_id):
                processor.run()
                
        elif choice == '4':
            print("退出程序")
            break
            
        else:
            print("无效选择，请重新输入")
        
        print()  # 空行

if __name__ == "__main__":
    # 方法1：直接快速启动
    # quick_start()
    
    # 方法2：使用命令行交互
    main()