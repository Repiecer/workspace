import cv2
import numpy as np
import time
from datetime import datetime

class RedDominantCameraFilter:
    """摄像头实时红色突出滤镜"""
    
    def __init__(self, camera_id=0, min_red_diff=10):
        """
        初始化摄像头滤镜
        
        参数:
        - camera_id: 摄像头ID (0通常是默认摄像头)
        - min_red_diff: 红色比其他通道的最小差值
        """
        self.camera_id = camera_id
        self.min_red_diff = min_red_diff
        self.cap = None
        self.is_running = False
        self.frame_count = 0
        self.start_time = None
        self.fps = 0
        self.red_percentage = 0
        
    def initialize_camera(self):
        """初始化摄像头"""
        print("正在初始化摄像头...")
        self.cap = cv2.VideoCapture(self.camera_id)
        
        if not self.cap.isOpened():
            print(f"错误：无法打开摄像头 {self.camera_id}")
            return False
        
        # 设置摄像头参数（可选）
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        # 获取实际设置
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        print(f"摄像头已打开: {width}x{height}, {fps}FPS")
        print("按以下键操作:")
        print("  'q' - 退出程序")
        print("  's' - 保存当前帧")
        print("  'r' - 重置统计")
        print("  '+' - 增加红色敏感度")
        print("  '-' - 降低红色敏感度")
        print("  'c' - 切换显示模式")
        print("-" * 50)
        
        return True
    
    def process_frame(self, frame):
        """
        处理单帧图像：红色不突出的像素转为黑白
        
        算法:
        1. 分离BGR通道
        2. 判断哪些像素红色突出 (R > G + diff 且 R > B + diff)
        3. 红色突出的像素保留原色
        4. 其他像素转为灰度
        """
        # 分离通道
        b, g, r = cv2.split(frame)
        
        # 创建红色突出的掩码
        red_dominant_mask = (r > g + self.min_red_diff) & (r > b + self.min_red_diff)
        
        # 计算灰度值 (使用标准灰度公式)
        gray_values = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)
        
        # 创建输出图像
        result = np.zeros_like(frame)
        
        # 红色突出的像素保留原色
        result[red_dominant_mask] = frame[red_dominant_mask]
        
        # 非红色突出的像素转为黑白
        non_red_mask = ~red_dominant_mask
        result[non_red_mask, 0] = gray_values[non_red_mask]  # B通道
        result[non_red_mask, 1] = gray_values[non_red_mask]  # G通道
        result[non_red_mask, 2] = gray_values[non_red_mask]  # R通道
        
        # 统计信息
        self.red_percentage = np.sum(red_dominant_mask) / (frame.shape[0] * frame.shape[1]) * 100
        
        return result, red_dominant_mask
    
    def add_overlay_info(self, frame, processed_frame, mode=0):
        """添加覆盖信息到图像"""
        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 根据显示模式创建不同的输出
        if mode == 0:
            # 模式0：并排显示
            output = np.hstack([frame, processed_frame])
            title = "Original  |  Red-Dominant Filter"
        elif mode == 1:
            # 模式1：上下显示
            output = np.vstack([frame, processed_frame])
            title = "Original (Top)  |  Filtered (Bottom)"
        elif mode == 2:
            # 模式2：只显示处理后的
            output = processed_frame.copy()
            title = "Red-Dominant Filter Only"
        else:
            # 模式3：只显示原始
            output = frame.copy()
            title = "Original Only"
        
        # 添加标题
        cv2.putText(output, title, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # 添加统计信息
        info_y = 60
        cv2.putText(output, f"Time: {current_time}", (10, info_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(output, f"FPS: {self.fps:.1f}", (10, info_y + 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(output, f"Frame: {self.frame_count}", (10, info_y + 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(output, f"Red sensitivity: {self.min_red_diff}", (10, info_y + 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(output, f"Red pixels: {self.red_percentage:.1f}%", (10, info_y + 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # 添加帮助文本
        help_text = "Q:Quit  S:Save  R:Reset  +/-:Sensitivity  C:Mode"
        cv2.putText(output, help_text, (10, output.shape[0] - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1)
        
        return output
    
    def calculate_fps(self):
        """计算实时FPS"""
        if self.start_time is None:
            self.start_time = time.time()
            return 0
        
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 0:
            self.fps = self.frame_count / elapsed_time
        return self.fps
    
    def save_snapshot(self, frame, processed_frame):
        """保存当前帧为图片"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存原始帧
        original_filename = f"snapshot_original_{timestamp}.jpg"
        cv2.imwrite(original_filename, frame)
        
        # 保存处理后的帧
        processed_filename = f"snapshot_processed_{timestamp}.jpg"
        cv2.imwrite(processed_filename, processed_frame)
        
        # 保存并排对比图
        combined = np.hstack([frame, processed_frame])
        combined_filename = f"snapshot_combined_{timestamp}.jpg"
        cv2.imwrite(combined_filename, combined)
        
        print(f"截图已保存: {original_filename}, {processed_filename}, {combined_filename}")
        return True
    
    def run(self):
        """主运行循环"""
        if not self.initialize_camera():
            return
        
        self.is_running = True
        self.start_time = time.time()
        self.frame_count = 0
        
        # 显示模式：0=并排，1=上下，2=只处理后，3=只原图
        display_mode = 0
        
        print("开始处理摄像头画面...")
        
        while self.is_running:
            # 读取帧
            ret, frame = self.cap.read()
            if not ret:
                print("错误：无法读取摄像头帧")
                break
            
            # 处理帧
            processed_frame, red_mask = self.process_frame(frame)
            
            # 更新计数
            self.frame_count += 1
            
            # 计算FPS（每秒更新一次）
            if self.frame_count % 30 == 0:
                self.calculate_fps()
            
            # 添加覆盖信息
            display_frame = self.add_overlay_info(frame, processed_frame, display_mode)
            
            # 显示结果
            cv2.imshow('Red Dominant Camera Filter', display_frame)
            
            # 处理键盘输入
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q') or key == 27:  # 'q' 或 ESC
                print("退出程序...")
                break
                
            elif key == ord('s'):
                self.save_snapshot(frame, processed_frame)
                
            elif key == ord('r'):
                # 重置统计
                self.frame_count = 0
                self.start_time = time.time()
                self.fps = 0
                print("统计已重置")
                
            elif key == ord('+') or key == ord('='):
                # 增加红色敏感度（需要更大的红色差值）
                self.min_red_diff = min(self.min_red_diff + 2, 100)
                print(f"红色敏感度增加: {self.min_red_diff}")
                
            elif key == ord('-') or key == ord('_'):
                # 降低红色敏感度（更容易识别红色）
                self.min_red_diff = max(self.min_red_diff - 2, 0)
                print(f"红色敏感度降低: {self.min_red_diff}")
                
            elif key == ord('c'):
                # 切换显示模式
                display_mode = (display_mode + 1) % 4
                modes = ["并排对比", "上下对比", "只显示处理", "只显示原始"]
                print(f"显示模式: {modes[display_mode]}")
                
            elif key == ord('m'):
                # 显示红色掩码
                red_mask_display = (red_mask * 255).astype(np.uint8)
                red_mask_display = cv2.cvtColor(red_mask_display, cv2.COLOR_GRAY2BGR)
                cv2.imshow('Red Mask Preview', red_mask_display)
                
            elif key != 255:  # 显示按下的键
                print(f"按键: {chr(key)} (ASCII: {key})")
        
        # 清理资源
        self.cleanup()
        
    def cleanup(self):
        """清理资源"""
        self.is_running = False
        
        if self.cap is not None:
            self.cap.release()
            print("摄像头已释放")
        
        cv2.destroyAllWindows()
        
        # 输出最终统计
        total_time = time.time() - self.start_time if self.start_time else 0
        print("\n" + "="*50)
        print("处理统计:")
        print(f"总帧数: {self.frame_count}")
        print(f"总时间: {total_time:.1f}秒")
        print(f"平均FPS: {self.frame_count/total_time:.1f}" if total_time > 0 else "平均FPS: N/A")
        print(f"最终红色像素比例: {self.red_percentage:.1f}%")
        print("程序结束")
        print("="*50)

# 简化版本（快速开始）
def simple_camera_filter():
    """
    简化版本的摄像头红色滤镜
    适合快速测试
    """
    print("启动红色突出滤镜（简化版）...")
    print("按 'q' 退出，'s' 保存截图")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("错误：无法打开摄像头")
        return
    
    # 设置摄像头分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    frame_count = 0
    start_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # 处理帧：红色不突出的转为黑白
        b, g, r = cv2.split(frame)
        
        # 判断红色突出像素
        red_dominant = (r > g) & (r > b)
        
        # 计算灰度值
        gray = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)
        
        # 创建结果
        result = frame.copy()
        result[~red_dominant, 0] = gray[~red_dominant]
        result[~red_dominant, 1] = gray[~red_dominant]
        result[~red_dominant, 2] = gray[~red_dominant]
        
        # 计算FPS
        elapsed = time.time() - start_time
        fps = frame_count / elapsed if elapsed > 0 else 0
        
        # 添加信息
        cv2.putText(result, f"FPS: {fps:.1f}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        red_pct = np.sum(red_dominant) / (frame.shape[0] * frame.shape[1]) * 100
        cv2.putText(result, f"Red: {red_pct:.1f}%", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # 显示
        cv2.imshow('Red Dominant Filter (Simple)', result)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(f'simple_snapshot_{timestamp}.jpg', result)
            print(f"截图已保存: simple_snapshot_{timestamp}.jpg")
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"处理了 {frame_count} 帧，平均FPS: {fps:.1f}")

# 命令行界面
def main():
    """主程序入口"""
    print("=" * 60)
    print("摄像头红色突出滤镜")
    print("=" * 60)
    print("功能说明：")
    print("- 保留红色突出的像素（红色比其他颜色更亮）")
    print("- 将红色不突出的像素转为黑白")
    print("- 实时处理摄像头画面")
    print()
    
    while True:
        print("请选择模式：")
        print("1. 完整功能版（推荐）")
        print("2. 简化快速版")
        print("3. 退出")
        
        choice = input("请输入选择 (1-3): ").strip()
        
        if choice == '1':
            print("\n启动完整功能版...")
            try:
                camera_id = input("输入摄像头ID (默认0，直接回车使用默认): ").strip()
                camera_id = int(camera_id) if camera_id else 0
                
                min_red_diff = input("输入红色敏感度 (默认10，建议5-30): ").strip()
                min_red_diff = int(min_red_diff) if min_red_diff else 10
                
                filter_app = RedDominantCameraFilter(camera_id=camera_id, 
                                                    min_red_diff=min_red_diff)
                filter_app.run()
                
            except ValueError:
                print("错误：请输入有效的数字")
            except Exception as e:
                print(f"程序出错: {e}")
                
        elif choice == '2':
            print("\n启动简化快速版...")
            simple_camera_filter()
            
        elif choice == '3':
            print("退出程序")
            break
            
        else:
            print("无效选择，请重新输入")
        
        print()  # 空行

# 直接运行版本（无需交互）
def direct_run(camera_id=0, min_red_diff=10):
    """直接运行，无需命令行交互"""
    print("正在启动摄像头红色突出滤镜...")
    print("按 'q' 退出程序")
    
    filter_app = RedDominantCameraFilter(camera_id=camera_id, 
                                        min_red_diff=min_red_diff)
    filter_app.run()

if __name__ == "__main__":
    # 方法1：直接运行（最简单）
    # direct_run(camera_id=0, min_red_diff=10)
    
    # 方法2：使用命令行交互界面
    main()
    
    # 方法3：运行简化版
    # simple_camera_filter()