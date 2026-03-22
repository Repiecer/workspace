import 'package:flutter/material.dart';
import 'dart:ui' as ui;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '卡片列表界面',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const CardListScreen(),
    );
  }
}

/// 主界面：底部两个按钮 + 主体卡片列表
class CardListScreen extends StatelessWidget {
  const CardListScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // 主体：可滚动的卡片列表
      body: Padding(
        padding: const EdgeInsets.only(top: 12, left: 12, right: 12),
        child: ListView.builder(
          itemCount: 15, // 生成15条卡片，可根据需要调整
          itemBuilder: (context, index) {
            return _buildCardItem(index);
          },
        ),
      ),
      // 底部保留两个按钮（从之前的界面沿用，略作样式统一）
      bottomNavigationBar: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // 第一个按钮：渐变文字
            ElevatedButton(
              onPressed: () {
                debugPrint('按钮1 点击');
              },
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(150, 48),
                backgroundColor: Colors.transparent,
                elevation: 0,
              ),
              child: Text(
                '按钮 1',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  foreground: Paint()
                    ..shader = ui.Gradient.linear(
                      const Offset(0, 0),
                      const Offset(150, 0),
                      [Colors.blue, Colors.purple, Colors.pink],
                      [0.0, 0.5, 1.0], // 三色渐变必须提供 colorStops
                    ),
                ),
              ),
            ),
            const SizedBox(width: 24),
            // 第二个按钮：绿色填充
            ElevatedButton(
              onPressed: () {
                debugPrint('按钮2 点击');
              },
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(150, 48),
                backgroundColor: Colors.green,
                foregroundColor: Colors.white,
                textStyle: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
              child: const Text('按钮 2'),
            ),
          ],
        ),
      ),
    );
  }

  /// 构建单条圆角卡片，内容随便填
  Widget _buildCardItem(int index) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12), // 卡片之间的间距
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16), // 圆角
      ),
      elevation: 4, // 轻微阴影
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          children: [
            // 左侧图标（随机颜色，增加视觉效果）
            Container(
              width: 50,
              height: 50,
              decoration: BoxDecoration(
                color: Colors.primaries[index % Colors.primaries.length]
                    .withOpacity(0.2),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(
                Icons.article,
                color: Colors.primaries[index % Colors.primaries.length],
              ),
            ),
            const SizedBox(width: 16),
            // 中间文字区域（扩展占满）
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '卡片标题 #${index + 1}',
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    '这是卡片 #${index + 1} 的描述内容，可以包含一些示例文本。',
                    style: TextStyle(fontSize: 14, color: Colors.grey[600]),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 8),
                  // 标签行
                  Row(
                    children: [
                      _buildTag('Flutter'),
                      const SizedBox(width: 8),
                      _buildTag('卡片示例'),
                    ],
                  ),
                ],
              ),
            ),
            // 右侧箭头
            Icon(Icons.chevron_right, color: Colors.grey[400]),
          ],
        ),
      ),
    );
  }

  /// 辅助方法：创建标签小圆块
  Widget _buildTag(String label) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: Colors.blue.withOpacity(0.1),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.blue.withOpacity(0.3)),
      ),
      child: Text(
        label,
        style: const TextStyle(fontSize: 12, color: Colors.blue),
      ),
    );
  }
}
