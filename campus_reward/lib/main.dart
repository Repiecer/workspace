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
      title: '简洁双按钮界面',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const HomePage(),
    );
  }
}

/// 极简界面：除了底部两个按钮，没有其他内容
class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // 将主体设为完全空的容器
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            'Text',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
        ],
      ),
      // 底部保留区域，只放置两个按钮
      bottomNavigationBar: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // 第一个按钮 - 渐变文字
            ElevatedButton(
              onPressed: () {
                debugPrint('按钮1 点击');
              },
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(150, 48),
                backgroundColor: Colors.transparent,
                elevation: 0,
                // 注意：这里不能设置 foregroundColor，否则会覆盖渐变色
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
                      [0.0, 0.5, 1.0],
                    ),
                ),
              ),
            ),

            const SizedBox(width: 24),

            // 第二个按钮 - 普通样式
            ElevatedButton(
              onPressed: () {
                debugPrint('按钮2 点击');
              },
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(150, 48),
                backgroundColor: Colors.green, // 背景色
                foregroundColor: Colors.white, // 文字颜色（统一在这里设置）
                textStyle: const TextStyle(
                  // 只设置字体样式，不设颜色
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
                elevation: 2,
                shape: RoundedRectangleBorder(
                  // 可选：添加圆角
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
}
