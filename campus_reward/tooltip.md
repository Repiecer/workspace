## Flutter 完整组件大全

| 分类 | 组件名 | 作用 | 常用程度 | 使用示例 |
|------|--------|------|----------|----------|
| **🏠 基础结构** | **MaterialApp** | 应用的根组件，配置主题、路由 | ⭐⭐⭐ | `MaterialApp(home: MyHomePage())` |
| | **Scaffold** | 页面基本结构（AppBar、Body、FAB） | ⭐⭐⭐ | `Scaffold(appBar: AppBar(), body: Center())` |
| | **AppBar** | 顶部应用栏 | ⭐⭐⭐ | `AppBar(title: Text('首页'))` |
| | **BottomNavigationBar** | 底部导航栏 | ⭐⭐⭐ | `BottomNavigationBar(items: [...])` |
| | **TabBar** | 选项卡 | ⭐⭐ | `TabBar(tabs: [Tab(text: '首页')])` |
| | **Drawer** | 侧边抽屉菜单 | ⭐⭐ | `Drawer(child: ListView())` |
| | **BottomSheet** | 底部弹出面板 | ⭐⭐ | `showBottomSheet(context: context, builder: ...)` |
| | **SnackBar** | 底部提示条 | ⭐⭐ | `ScaffoldMessenger.of(context).showSnackBar()` |
| | **FloatingActionButton** | 悬浮按钮 | ⭐⭐⭐ | `FloatingActionButton(onPressed: () {})` |
| | **PersistentBottomSheet** | 持久底部面板 | ⭐ | `Scaffold.of(context).showBottomSheet()` |
| | **CupertinoApp** | iOS风格应用根组件 | ⭐ | `CupertinoApp(home: CupertinoPageScaffold())` |
| | **CupertinoPageScaffold** | iOS风格页面结构 | ⭐ | `CupertinoPageScaffold(child: Center())` |
| **📦 布局组件** | **Container** | 多功能容器（宽高、边距、背景） | ⭐⭐⭐ | `Container(width: 100, height: 50, color: Colors.blue)` |
| | **Row** | 水平排列子组件 | ⭐⭐⭐ | `Row(children: [Text('A'), Text('B')])` |
| | **Column** | 垂直排列子组件 | ⭐⭐⭐ | `Column(children: [Text('A'), Text('B')])` |
| | **Stack** | 层叠布局（重叠） | ⭐⭐⭐ | `Stack(children: [Image.network('url'), Text('文字')])` |
| | **Center** | 居中布局 | ⭐⭐⭐ | `Center(child: CircularProgressIndicator())` |
| | **Padding** | 内边距 | ⭐⭐⭐ | `Padding(padding: EdgeInsets.all(8), child: Text('Hello'))` |
| | **Align** | 对齐布局 | ⭐⭐ | `Align(alignment: Alignment.topRight, child: Text('右上'))` |
| | **AspectRatio** | 固定宽高比 | ⭐⭐ | `AspectRatio(aspectRatio: 16/9, child: Container())` |
| | **ConstrainedBox** | 约束子组件的大小 | ⭐⭐ | `ConstrainedBox(constraints: BoxConstraints(maxWidth: 200))` |
| | **LimitedBox** | 无约束时限制大小 | ⭐ | `LimitedBox(maxWidth: 100, child: Text('...'))` |
| | **OverflowBox** | 允许子组件超出父组件 | ⭐ | `OverflowBox(minWidth: 200, child: Container())` |
| | **SizedBox** | 固定大小的盒子 | ⭐⭐⭐ | `SizedBox(width: 20, height: 20)` |
| | **SizedOverflowBox** | 固定大小但允许溢出 | ⭐ | `SizedOverflowBox(size: Size(100, 100), child: ...)` |
| | **FittedBox** | 缩放子组件以适应父组件 | ⭐⭐ | `FittedBox(child: Text('很长的文本'))` |
| | **Expanded** | 填充Row/Column剩余空间 | ⭐⭐⭐ | `Expanded(child: Text('占满剩余空间'))` |
| | **Flexible** | 灵活占满剩余空间 | ⭐⭐ | `Flexible(flex: 2, child: Text('灵活比例'))` |
| | **Wrap** | 自动换行/换列 | ⭐⭐ | `Wrap(children: [Chip(...), Chip(...)])` |
| | **Flow** | 自定义流式布局 | ⭐ | `Flow(delegate: MyFlowDelegate(), children: [...])` |
| | **Table** | 表格布局 | ⭐⭐ | `Table(children: [TableRow(children: [Text('A'), Text('B')])])` |
| | **LayoutBuilder** | 根据父组件约束动态构建 | ⭐⭐ | `LayoutBuilder(builder: (context, constraints) {...})` |
| | **CustomMultiChildLayout** | 自定义多子组件布局 | ⭐ | `CustomMultiChildLayout(delegate: MyDelegate())` |
| | **IndexedStack** | 只显示一个子组件 | ⭐ | `IndexedStack(index: 0, children: [Text('A'), Text('B')])` |
| | **FractionallySizedBox** | 按比例占据父组件空间 | ⭐⭐ | `FractionallySizedBox(widthFactor: 0.5, child: ...)` |
| | **Transform** | 变换（旋转、缩放、平移） | ⭐⭐ | `Transform.rotate(angle: pi/4, child: Text('旋转'))` |
| | **RotatedBox** | 旋转子组件 | ⭐ | `RotatedBox(quarterTurns: 1, child: Text('旋转90度'))` |
| | **Offstage** | 隐藏子组件 | ⭐ | `Offstage(offstage: true, child: Text('隐藏'))` |
| | **Opacity** | 透明度 | ⭐⭐ | `Opacity(opacity: 0.5, child: Text('半透明'))` |
| | **Visibility** | 控制可见性 | ⭐⭐ | `Visibility(visible: false, child: Text('隐藏'))` |
| **📝 文本与图标** | **Text** | 显示文本 | ⭐⭐⭐ | `Text('Hello', style: TextStyle(fontSize: 20))` |
| | **RichText** | 富文本 | ⭐⭐ | `RichText(text: TextSpan(text: 'Hello', style: ...))` |
| | **DefaultTextStyle** | 设置默认文本样式 | ⭐⭐ | `DefaultTextStyle(style: TextStyle(color: red), child: ...)` |
| | **SelectableText** | 可选择的文本 | ⭐⭐ | `SelectableText('可复制文本')` |
| | **Icon** | 图标 | ⭐⭐⭐ | `Icon(Icons.favorite, color: Colors.red)` |
| | **IconTheme** | 图标主题 | ⭐ | `IconTheme(data: IconThemeData(size: 30), child: ...)` |
| | **Image** | 图片 | ⭐⭐⭐ | `Image.network('url'), Image.asset('assets/icon.png')` |
| | **AssetImage** | 资源图片 | ⭐⭐ | `AssetImage('assets/image.png')` |
| | **NetworkImage** | 网络图片 | ⭐⭐ | `NetworkImage('https://example.com/image.jpg')` |
| | **FileImage** | 文件图片 | ⭐ | `FileImage(File('/path/to/image.jpg'))` |
| | **MemoryImage** | 内存图片 | ⭐ | `MemoryImage(Uint8List bytes)` |
| | **ExactAssetImage** | 精确资源图片 | ⭐ | `ExactAssetImage('assets/image.png')` |
| | **FadeInImage** | 淡入淡出图片 | ⭐⭐ | `FadeInImage(placeholder: AssetImage('loading.gif'), image: NetworkImage('url'))` |
| | **CircleAvatar** | 圆形头像 | ⭐⭐⭐ | `CircleAvatar(backgroundImage: NetworkImage('url'))` |
| **🔘 按钮与交互** | **ElevatedButton** | 凸起按钮（Material 3） | ⭐⭐⭐ | `ElevatedButton(onPressed: () {}, child: Text('点击'))` |
| | **TextButton** | 文本按钮 | ⭐⭐⭐ | `TextButton(onPressed: () {}, child: Text('取消'))` |
| | **OutlinedButton** | 边框按钮 | ⭐⭐⭐ | `OutlinedButton(onPressed: () {}, child: Text('提交'))` |
| | **IconButton** | 图标按钮 | ⭐⭐⭐ | `IconButton(icon: Icon(Icons.add), onPressed: () {})` |
| | **FloatingActionButton** | 悬浮按钮 | ⭐⭐⭐ | `FloatingActionButton(child: Icon(Icons.add), onPressed: () {})` |
| | **DropdownButton** | 下拉按钮 | ⭐⭐ | `DropdownButton(items: [...], onChanged: () {})` |
| | **PopupMenuButton** | 弹出菜单按钮 | ⭐⭐ | `PopupMenuButton(itemBuilder: (context) => [...])` |
| | **BackButton** | 返回按钮 | ⭐⭐ | `BackButton(onPressed: () {})` |
| | **CloseButton** | 关闭按钮 | ⭐⭐ | `CloseButton(onPressed: () {})` |
| | **CupertinoButton** | iOS风格按钮 | ⭐ | `CupertinoButton(child: Text('按钮'), onPressed: () {})` |
| | **RawMaterialButton** | 原始Material按钮 | ⭐ | `RawMaterialButton(onPressed: () {}, child: Text('按钮'))` |
| | **MaterialButton** | Material按钮（旧版） | ⭐ | `MaterialButton(onPressed: () {}, child: Text('按钮'))` |
| | **FlatButton** | 扁平按钮（已弃用） | ⭐ | `FlatButton(onPressed: () {}, child: Text('按钮'))` |
| | **ButtonBar** | 按钮栏 | ⭐⭐ | `ButtonBar(children: [TextButton(), ElevatedButton()])` |
| | **GestureDetector** | 手势检测 | ⭐⭐⭐ | `GestureDetector(onTap: () {}, child: Container())` |
| | **InkWell** | 水波纹效果 | ⭐⭐⭐ | `InkWell(onTap: () {}, child: Container())` |
| | **InkResponse** | 自定义水波纹 | ⭐ | `InkResponse(onTap: () {}, child: Container())` |
| | **Listener** | 原始指针事件 | ⭐ | `Listener(onPointerDown: (event) {}, child: ...)` |
| | **AbsorbPointer** | 阻止点击事件 | ⭐⭐ | `AbsorbPointer(absorbing: true, child: Button())` |
| | **IgnorePointer** | 忽略点击事件 | ⭐ | `IgnorePointer(ignoring: true, child: Button())` |
| | **Draggable** | 可拖拽组件 | ⭐⭐ | `Draggable(child: Icon(Icons.drag_handle), feedback: ...)` |
| | **DragTarget** | 拖拽目标 | ⭐⭐ | `DragTarget(onAccept: (data) {}, builder: ...)` |
| | **LongPressDraggable** | 长按拖拽 | ⭐ | `LongPressDraggable(child: ...)` |
| | **Tooltip** | 提示文本 | ⭐⭐ | `Tooltip(message: '提示', child: Icon(Icons.info))` |
| **📋 输入组件** | **TextField** | 文本输入框 | ⭐⭐⭐ | `TextField(decoration: InputDecoration(labelText: '用户名'))` |
| | **TextFormField** | 表单文本输入框 | ⭐⭐⭐ | `TextFormField(validator: (value) {...})` |
| | **Checkbox** | 复选框 | ⭐⭐⭐ | `Checkbox(value: true, onChanged: (value) {})` |
| | **CheckboxListTile** | 带标题的复选框 | ⭐⭐ | `CheckboxListTile(title: Text('选项'), value: true, onChanged: ...)` |
| | **Radio** | 单选框 | ⭐⭐⭐ | `Radio(value: 1, groupValue: 1, onChanged: (value) {})` |
| | **RadioListTile** | 带标题的单选框 | ⭐⭐ | `RadioListTile(title: Text('选项'), value: 1, groupValue: 1, onChanged: ...)` |
| | **Switch** | 开关 | ⭐⭐⭐ | `Switch(value: true, onChanged: (value) {})` |
| | **SwitchListTile** | 带标题的开关 | ⭐⭐ | `SwitchListTile(title: Text('开启'), value: true, onChanged: ...)` |
| | **Slider** | 滑动条 | ⭐⭐⭐ | `Slider(value: 50, min: 0, max: 100, onChanged: (value) {})` |
| | **RangeSlider** | 范围滑动条 | ⭐⭐ | `RangeSlider(values: RangeValues(20, 80), onChanged: ...)` |
| | **CupertinoSlider** | iOS风格滑动条 | ⭐ | `CupertinoSlider(value: 50, onChanged: (value) {})` |
| | **DropdownButtonFormField** | 表单下拉框 | ⭐⭐ | `DropdownButtonFormField(items: [...], onChanged: ...)` |
| | **DatePicker** | 日期选择器 | ⭐⭐⭐ | `showDatePicker(context: context, initialDate: DateTime.now())` |
| | **TimePicker** | 时间选择器 | ⭐⭐ | `showTimePicker(context: context, initialTime: TimeOfDay.now())` |
| | **CupertinoDatePicker** | iOS风格日期选择器 | ⭐ | `CupertinoDatePicker(onDateTimeChanged: ...)` |
| | **CupertinoTimerPicker** | iOS风格时间选择器 | ⭐ | `CupertinoTimerPicker(onTimerDurationChanged: ...)` |
| | **Stepper** | 步进器 | ⭐⭐ | `Stepper(steps: [Step(title: Text('步骤1'))])` |
| | **Form** | 表单 | ⭐⭐⭐ | `Form(key: _formKey, child: Column())` |
| | **FormField** | 自定义表单字段 | ⭐ | `FormField(builder: (state) {...})` |
| | **RawKeyboardListener** | 键盘事件监听 | ⭐ | `RawKeyboardListener(onKey: (event) {}, child: ...)` |
| **📜 列表与滚动** | **ListView** | 可滚动列表 | ⭐⭐⭐ | `ListView(children: [Text('A'), Text('B')])` |
| | **ListView.builder** | 高效构建大量列表项 | ⭐⭐⭐ | `ListView.builder(itemCount: 100, itemBuilder: (context, index) {...})` |
| | **ListView.separated** | 带分割线的列表 | ⭐⭐ | `ListView.separated(itemBuilder: ..., separatorBuilder: ...)` |
| | **GridView** | 网格列表 | ⭐⭐⭐ | `GridView.count(crossAxisCount: 2, children: [...])` |
| | **GridView.builder** | 高效网格 | ⭐⭐ | `GridView.builder(gridDelegate: ..., itemBuilder: ...)` |
| | **GridView.count** | 指定列数的网格 | ⭐⭐⭐ | `GridView.count(crossAxisCount: 2, children: [...])` |
| | **GridView.extent** | 指定最大宽度的网格 | ⭐⭐ | `GridView.extent(maxCrossAxisExtent: 100, children: [...])` |
| | **PageView** | 页面滑动切换 | ⭐⭐⭐ | `PageView(children: [Page1(), Page2()])` |
| | **PageView.builder** | 高效页面切换 | ⭐⭐ | `PageView.builder(itemBuilder: (context, index) {...})` |
| | **SingleChildScrollView** | 单个可滚动组件 | ⭐⭐⭐ | `SingleChildScrollView(child: Column(...))` |
| | **CustomScrollView** | 自定义滚动效果 | ⭐⭐ | `CustomScrollView(slivers: [SliverAppBar(), SliverList()])` |
| | **Scrollbar** | 滚动条 | ⭐⭐ | `Scrollbar(child: ListView(...))` |
| | **RefreshIndicator** | 下拉刷新 | ⭐⭐⭐ | `RefreshIndicator(onRefresh: () async {...}, child: ListView())` |
| | **NotificationListener** | 监听滚动通知 | ⭐⭐ | `NotificationListener(onNotification: (notification) {...})` |
| | **ScrollConfiguration** | 滚动配置 | ⭐ | `ScrollConfiguration(behavior: MyBehavior(), child: ...)` |
| | **ReorderableListView** | 可重新排序的列表 | ⭐⭐ | `ReorderableListView(onReorder: (oldIndex, newIndex) {...})` |
| | **AnimatedList** | 动画列表 | ⭐⭐ | `AnimatedList(itemBuilder: (context, index, animation) {...})` |
| | **SliverAppBar** | 可伸缩AppBar | ⭐⭐⭐ | `SliverAppBar(expandedHeight: 200, flexibleSpace: ...)` |
| | **SliverList** | Sliver列表 | ⭐⭐ | `SliverList(delegate: SliverChildBuilderDelegate(...))` |
| | **SliverGrid** | Sliver网格 | ⭐⭐ | `SliverGrid(delegate: ..., gridDelegate: ...)` |
| | **SliverFillRemaining** | 填充剩余空间 | ⭐ | `SliverFillRemaining(child: Center(child: Text('完成')))` |
| | **SliverPadding** | Sliver内边距 | ⭐⭐ | `SliverPadding(padding: EdgeInsets.all(8), sliver: ...)` |
| | **SliverToBoxAdapter** | 普通Widget转Sliver | ⭐⭐ | `SliverToBoxAdapter(child: Container(height: 100))` |
| **📊 卡片与信息** | **Card** | 卡片 | ⭐⭐⭐ | `Card(child: ListTile(title: Text('标题')))` |
| | **ListTile** | 列表项 | ⭐⭐⭐ | `ListTile(leading: Icon(Icons.star), title: Text('标题'))` |
| | **ListTile.divideTiles** | 带分割线的列表项 | ⭐⭐ | `ListTile.divideTiles(context: context, tiles: [...])` |
| | **AboutListTile** | 关于对话框列表项 | ⭐ | `AboutListTile(icon: Icon(Icons.info), child: Text('关于'))` |
| | **CheckboxListTile** | 带复选框的列表项 | ⭐⭐ | `CheckboxListTile(title: Text('选项'), value: true, onChanged: ...)` |
| | **RadioListTile** | 带单选框的列表项 | ⭐⭐ | `RadioListTile(title: Text('选项'), value: 1, groupValue: 1)` |
| | **SwitchListTile** | 带开关的列表项 | ⭐⭐ | `SwitchListTile(title: Text('开启'), value: true, onChanged: ...)` |
| | **ExpansionTile** | 可展开列表项 | ⭐⭐⭐ | `ExpansionTile(title: Text('更多'), children: [Text('内容')])` |
| | **DataTable** | 数据表格 | ⭐⭐ | `DataTable(columns: [...], rows: [...])` |
| | **DataGrid** | 高级数据表格 | ⭐ | `DataGrid(columns: [...], rows: [...])` |
| | **PaginatedDataTable** | 分页数据表格 | ⭐ | `PaginatedDataTable(columns: [...], source: ...)` |
| | **Chip** | 标签 | ⭐⭐⭐ | `Chip(label: Text('标签'))` |
| | **InputChip** | 输入标签 | ⭐⭐ | `InputChip(label: Text('标签'), onPressed: () {})` |
| | **ChoiceChip** | 选择标签 | ⭐⭐ | `ChoiceChip(label: Text('选项'), selected: true)` |
| | **FilterChip** | 过滤标签 | ⭐⭐ | `FilterChip(label: Text('过滤'), selected: true)` |
| | **ActionChip** | 操作标签 | ⭐⭐ | `ActionChip(label: Text('操作'), onPressed: () {})` |
| | **Avatar** | 头像 | ⭐⭐ | `Avatar(child: Text('A'))` |
| | **CircleAvatar** | 圆形头像 | ⭐⭐⭐ | `CircleAvatar(backgroundImage: NetworkImage('url'))` |
| | **Badge** | 徽标 | ⭐⭐ | `Badge(label: Text('3'), child: Icon(Icons.notifications))` |
| **⏳ 进度与加载** | **LinearProgressIndicator** | 线性进度条 | ⭐⭐⭐ | `LinearProgressIndicator(value: 0.5)` |
| | **CircularProgressIndicator** | 圆形进度条 | ⭐⭐⭐ | `CircularProgressIndicator()` |
| | **RefreshProgressIndicator** | 刷新进度条 | ⭐ | `RefreshProgressIndicator()` |
| | **CupertinoActivityIndicator** | iOS风格加载 | ⭐ | `CupertinoActivityIndicator()` |
| | **CircularProgressIndicator.adaptive** | 自适应进度条 | ⭐⭐ | `CircularProgressIndicator.adaptive()` |
| | **ProgressIndicatorTheme** | 进度条主题 | ⭐ | `ProgressIndicatorTheme(data: ...)` |
| **🎨 装饰与效果** | **DecoratedBox** | 装饰盒子 | ⭐⭐ | `DecoratedBox(decoration: BoxDecoration(color: Colors.blue))` |
| | **BoxDecoration** | 盒子装饰 | ⭐⭐⭐ | `BoxDecoration(color: Colors.blue, borderRadius: BorderRadius.circular(10))` |
| | **ShapeDecoration** | 形状装饰 | ⭐ | `ShapeDecoration(shape: CircleBorder(), color: Colors.blue)` |
| | **FlutterLogo** | Flutter logo | ⭐ | `FlutterLogo(size: 100)` |
| | **Placeholder** | 占位符 | ⭐⭐ | `Placeholder(color: Colors.grey)` |
| | **Divider** | 分割线 | ⭐⭐⭐ | `Divider(thickness: 1, color: Colors.grey)` |
| | **VerticalDivider** | 垂直分割线 | ⭐⭐ | `VerticalDivider(width: 1)` |
| | **ClipRect** | 矩形裁剪 | ⭐⭐ | `ClipRect(child: Image.network('url'))` |
| | **ClipRRect** | 圆角矩形裁剪 | ⭐⭐⭐ | `ClipRRect(borderRadius: BorderRadius.circular(10), child: Image(...))` |
| | **ClipOval** | 圆形裁剪 | ⭐⭐ | `ClipOval(child: Image.network('url'))` |
| | **ClipPath** | 自定义路径裁剪 | ⭐ | `ClipPath(clipper: MyClipper(), child: ...)` |
| | **CustomPaint** | 自定义绘制 | ⭐⭐ | `CustomPaint(painter: MyPainter(), child: ...)` |
| | **ColorFiltered** | 颜色滤镜 | ⭐ | `ColorFiltered(colorFilter: ColorFilter.mode(Colors.red, BlendMode.color))` |
| | **BackdropFilter** | 背景模糊 | ⭐⭐ | `BackdropFilter(filter: ImageFilter.blur(sigmaX: 5, sigmaY: 5))` |
| | **ShaderMask** | 着色器遮罩 | ⭐ | `ShaderMask(shaderCallback: (bounds) {...})` |
| | **Opacity** | 透明度 | ⭐⭐⭐ | `Opacity(opacity: 0.5, child: Text('半透明'))` |
| | **AnimatedOpacity** | 带动画的透明度 | ⭐⭐⭐ | `AnimatedOpacity(opacity: 0.5, duration: Duration(seconds: 1))` |
| **🔄 动画组件** | **AnimatedContainer** | 动画容器 | ⭐⭐⭐ | `AnimatedContainer(width: 100, duration: Duration(seconds: 1))` |
| | **AnimatedCrossFade** | 交叉淡入淡出 | ⭐⭐ | `AnimatedCrossFade(firstChild: A(), secondChild: B(), crossFadeState: ...)` |
| | **AnimatedPadding** | 动画边距 | ⭐⭐ | `AnimatedPadding(padding: EdgeInsets.all(20), duration: ...)` |
| | **AnimatedPositioned** | 动画定位 | ⭐⭐ | `AnimatedPositioned(left: 100, duration: ...)` |
| | **AnimatedSwitcher** | 切换动画 | ⭐⭐⭐ | `AnimatedSwitcher(child: Text('$_counter'), duration: ...)` |
| | **AnimatedOpacity** | 透明度动画 | ⭐⭐⭐ | `AnimatedOpacity(opacity: 0.5, duration: ...)` |
| | **AnimatedBuilder** | 动画构建器 | ⭐⭐ | `AnimatedBuilder(animation: _animation, builder: (context, child) {...})` |
| | **AnimatedWidget** | 动画Widget基类 | ⭐ | `class MyAnimatedWidget extends AnimatedWidget {...}` |
| | **TweenAnimationBuilder** | 补间动画构建器 | ⭐⭐⭐ | `TweenAnimationBuilder(tween: Tween(begin: 0, end: 1), builder: ...)` |
| | **SlideTransition** | 滑动动画 | ⭐⭐ | `SlideTransition(position: _animation, child: ...)` |
| | **ScaleTransition** | 缩放动画 | ⭐⭐ | `ScaleTransition(scale: _animation, child: ...)` |
| | **RotationTransition** | 旋转动画 | ⭐⭐ | `RotationTransition(turns: _animation, child: ...)` |
| | **FadeTransition** | 淡入淡出动画 | ⭐⭐ | `FadeTransition(opacity: _animation, child: ...)` |
| | **SizeTransition** | 尺寸变化动画 | ⭐ | `SizeTransition(sizeFactor: _animation, child: ...)` |
| | **PositionedTransition** | 定位动画 | ⭐ | `PositionedTransition(rect: _animation, child: ...)` |
| | **AlignTransition** | 对齐动画 | ⭐ | `AlignTransition(alignment: _animation, child: ...)` |
| | **Hero** | 共享元素动画 | ⭐⭐⭐ | `Hero(tag: 'image', child: Image.network('url'))` |
| | **FadeInImage** | 图片淡入 | ⭐⭐ | `FadeInImage(placeholder: AssetImage('loading.gif'), image: NetworkImage('url'))` |
| **🔔 提示与弹窗** | **AlertDialog** | 警告对话框 | ⭐⭐⭐ | `AlertDialog(title: Text('提示'), content: Text('确定吗？'))` |
| | **SimpleDialog** | 简单对话框 | ⭐⭐ | `SimpleDialog(title: Text('选择'), children: [...]` |
| | **Dialog** | 自定义对话框 | ⭐⭐ | `Dialog(child: Container(width: 200, height: 200))` |
| | **AboutDialog** | 关于对话框 | ⭐ | `AboutDialog(applicationName: 'App')` |
| | **CupertinoAlertDialog** | iOS风格警告框 | ⭐ | `CupertinoAlertDialog(title: Text('提示'), content: Text('确定吗？'))` |
| | **SnackBar** | 底部提示条 | ⭐⭐⭐ | `SnackBar(content: Text('保存成功'))` |
| | **BottomSheet** | 底部面板 | ⭐⭐⭐ | `showBottomSheet(context: context, builder: (context) => Container())` |
| | **ModalBottomSheet** | 模态底部面板 | ⭐⭐ | `showModalBottomSheet(context: context, builder: (context) => ...)` |
| | **Tooltip** | 提示文本 | ⭐⭐⭐ | `Tooltip(message: '提示', child: Icon(Icons.info))` |
| | **MaterialBanner** | 横幅提示 | ⭐⭐ | `MaterialBanner(content: Text('提示'), actions: [TextButton(...)])` |
| | **CupertinoActionSheet** | iOS操作面板 | ⭐ | `CupertinoActionSheet(title: Text('选择'), actions: [...])` |
| | **PopupMenuDivider** | 弹出菜单分割线 | ⭐ | `PopupMenuDivider()` |
| | **PopupMenuItem** | 弹出菜单项 | ⭐⭐ | `PopupMenuItem(child: Text('选项'))` |
| **🧭 导航与路由** | **Navigator** | 导航器 | ⭐⭐⭐ | `Navigator.push(context, MaterialPageRoute(builder: (context) => Page()))` |
| | **MaterialPageRoute** | 页面路由 | ⭐⭐⭐ | `MaterialPageRoute(builder: (context) => SecondPage())` |
| | **CupertinoPageRoute** | iOS风格路由 | ⭐ | `CupertinoPageRoute(builder: (context) => SecondPage())` |
| | **PageRouteBuilder** | 自定义路由动画 | ⭐⭐ | `PageRouteBuilder(pageBuilder: (context, animation, secondaryAnimation) => ...)` |
| | **ModalRoute** | 模态路由基类 | ⭐ | `ModalRoute.of(context)` |
| | **RouteObserver** | 路由观察器 | ⭐ | `RouteObserver<PageRoute>()` |
| | **HeroController** | Hero动画控制器 | ⭐ | `HeroController()` |
| | **WillPopScope** | 拦截返回键 | ⭐⭐⭐ | `WillPopScope(onWillPop: () async => false, child: ...)` |
| | **Router** | 路由（声明式导航） | ⭐ | `Router(routerDelegate: myRouterDelegate)` |
| | **RouterDelegate** | 路由委托 | ⭐ | `class MyRouterDelegate extends RouterDelegate {...}` |
| | **RouteInformationParser** | 路由信息解析 | ⭐ | `class MyRouteInformationParser extends RouteInformationParser {...}` |
| **🎯 特殊用途** | **InheritedWidget** | 数据共享 | ⭐⭐ | `class MyInherited extends InheritedWidget {...}` |
| | **InheritedModel** | 精细数据共享 | ⭐ | `InheritedModel<MyType>` |
| | **InheritedTheme** | 主题继承 | ⭐ | `InheritedTheme(capture: (context) => Theme.of(context))` |
| | **MediaQuery** | 媒体信息查询 | ⭐⭐⭐ | `MediaQuery.of(context).size.width` |
| | **MediaQuery.removePadding** | 移除边距 | ⭐ | `MediaQuery.removePadding(context: context, child: ...)` |
| | **MediaQuery.removeViewInsets** | 移除视图内边距 | ⭐ | `MediaQuery.removeViewInsets(context: context, child: ...)` |
| | **SafeArea** | 安全区域 | ⭐⭐⭐ | `SafeArea(child: Text('内容'))` |
| | **Directionality** | 文本方向 | ⭐⭐ | `Directionality(textDirection: TextDirection.ltr, child: ...)` |
| | **Localizations** | 本地化 | ⭐⭐ | `Localizations.override( ... )` |
| | **DefaultAssetBundle** | 默认资源包 | ⭐ | `DefaultAssetBundle.of(context)` |
| | **Builder** | 获取Context | ⭐⭐⭐ | `Builder(builder: (context) => Text('Hello'))` |
| | **StatefulBuilder** | 局部状态构建器 | ⭐⭐ | `StatefulBuilder(builder: (context, setState) {...})` |
| | **ValueListenableBuilder** | 值监听构建器 | ⭐⭐⭐ | `ValueListenableBuilder(valueListenable: counter, builder: ...)` |
| | **StreamBuilder** | 流构建器 | ⭐⭐⭐ | `StreamBuilder(stream: myStream, builder: ...)` |
| | **FutureBuilder** | 异步构建器 | ⭐⭐⭐ | `FutureBuilder(future: myFuture, builder: ...)` |
| | **OrientationBuilder** | 方向构建器 | ⭐⭐ | `OrientationBuilder(builder: (context, orientation) {...})` |
| | **LayoutBuilder** | 布局构建器 | ⭐⭐ | `LayoutBuilder(builder: (context, constraints) {...})` |
| | **CustomMultiChildLayout** | 自定义多子布局 | ⭐ | `CustomMultiChildLayout(delegate: MyDelegate())` |
| | **CustomSingleChildLayout** | 自定义单子布局 | ⭐ | `CustomSingleChildLayout(delegate: MyDelegate())` |
| **📱 平台特定** | **CupertinoApp** | iOS应用根组件 | ⭐ | `CupertinoApp(home: CupertinoPageScaffold())` |
| | **CupertinoPageScaffold** | iOS页面结构 | ⭐ | `CupertinoPageScaffold(child: Center())` |
| | **CupertinoTabScaffold** | iOS标签页结构 | ⭐ | `CupertinoTabScaffold(tabBar: CupertinoTabBar(items: [...])` |
| | **CupertinoNavigationBar** | iOS导航栏 | ⭐ | `CupertinoNavigationBar(middle: Text('标题'))` |
| | **CupertinoTabBar** | iOS标签栏 | ⭐ | `CupertinoTabBar(items: [BottomNavigationBarItem(...)])` |
| | **CupertinoButton** | iOS按钮 | ⭐ | `CupertinoButton(child: Text('按钮'), onPressed: () {})` |
| | **CupertinoTextField** | iOS文本输入 | ⭐ | `CupertinoTextField(placeholder: '输入')` |
| | **CupertinoSlider** | iOS滑块 | ⭐ | `CupertinoSlider(value: 50, onChanged: (value) {})` |
| | **CupertinoSwitch** | iOS开关 | ⭐ | `CupertinoSwitch(value: true, onChanged: (value) {})` |
| | **CupertinoSegmentedControl** | iOS分段控制 | ⭐ | `CupertinoSegmentedControl(children: {...})` |
| | **CupertinoPicker** | iOS选择器 | ⭐ | `CupertinoPicker(children: [...], onSelectedItemChanged: ...)` |
| | **CupertinoDatePicker** | iOS日期选择器 | ⭐ | `CupertinoDatePicker(onDateTimeChanged: ...)` |
| | **CupertinoTimerPicker** | iOS计时器选择器 | ⭐ | `CupertinoTimerPicker(onTimerDurationChanged: ...)` |
| | **CupertinoActionSheet** | iOS操作面板 | ⭐ | `CupertinoActionSheet(title: Text('选择'), actions: [...])` |
| | **CupertinoAlertDialog** | iOS警告框 | ⭐ | `CupertinoAlertDialog(title: Text('提示'), content: Text('确定吗？'))` |
| | **CupertinoActivityIndicator** | iOS加载指示器 | ⭐ | `CupertinoActivityIndicator()` |
| | **CupertinoContextMenu** | iOS上下文菜单 | ⭐ | `CupertinoContextMenu(actions: [...], child: ...)` |
| | **CupertinoPopupSurface** | iOS弹出层 | ⭐ | `CupertinoPopupSurface(child: ...)` |
| | **CupertinoSliverNavigationBar** | iOS可伸缩导航栏 | ⭐ | `CupertinoSliverNavigationBar(largeTitle: Text('标题'))` |
| | **CupertinoSliverRefreshControl** | iOS下拉刷新 | ⭐ | `CupertinoSliverRefreshControl(onRefresh: () async {...})` |
| **📦 其他实用组件** | **Theme** | 主题设置 | ⭐⭐⭐ | `Theme(data: ThemeData.light(), child: ...)` |
| | **Theme.of** | 获取主题 | ⭐⭐⭐ | `Theme.of(context).primaryColor` |
| | **MediaQuery** | 媒体查询 | ⭐⭐⭐ | `MediaQuery.of(context).size` |
| | **Localizations** | 本地化 | ⭐⭐ | `Localizations.override( ... )` |
| | **DefaultTextStyle** | 默认文本样式 | ⭐⭐ | `DefaultTextStyle(style: TextStyle(color: red), child: ...)` |
| | **DefaultAssetBundle** | 默认资源包 | ⭐ | `DefaultAssetBundle.of(context).loadString('assets/data.json')` |
| | **Focus** | 焦点管理 | ⭐⭐ | `Focus(onFocusChange: (hasFocus) {...}, child: ...)` |
| | **FocusScope** | 焦点作用域 | ⭐ | `FocusScope.of(context).requestFocus(myFocusNode)` |
| | **Shortcuts** | 快捷键 | ⭐ | `Shortcuts(shortcuts: {...}, child: ...)` |
| | **Actions** | 动作 | ⭐ | `Actions(dispatcher: ...)` |
| | **Intent** | 意图 | ⭐ | `class MyIntent extends Intent {...}` |
| | **RawKeyboardListener** | 键盘监听 | ⭐ | `RawKeyboardListener(onKey: (event) {...}, child: ...)` |
| | **RawGestureDetector** | 原始手势检测 | ⭐ | `RawGestureDetector(gestures: {...}, child: ...)` |
| | **Semantics** | 语义化（辅助功能） | ⭐ | `Semantics(label: '按钮', child: ...)` |
| | **MergeSemantics** | 合并语义 | ⭐ | `MergeSemantics(child: ...)` |
| | **ExcludeSemantics** | 排除语义 | ⭐ | `ExcludeSemantics(child: ...)` |
| | **BlockSemantics** | 阻止语义 | ⭐ | `BlockSemantics(child: ...)` |
| | **Builder** | 获取Context | ⭐⭐⭐ | `Builder(builder: (context) => Text('Hello'))` |
| | **StatefulBuilder** | 局部状态 | ⭐⭐ | `StatefulBuilder(builder: (context, setState) {...})` |
| | **TickerMode** | 控制动画 | ⭐ | `TickerMode(enabled: false, child: ...)` |
| | **PerformanceOverlay** | 性能覆盖层 | ⭐ | `PerformanceOverlay.allEnabled()` |
| | **Checkerboard** | 棋盘格（调试用） | ⭐ | `CheckerboardRasterCacheImages()` |

---

## 常用程度说明

- ⭐⭐⭐ **必用**：几乎每个应用都会用到
- ⭐⭐ **常用**：经常使用，但不是必须
- ⭐ **偶尔用**：特定场景才用

## 使用建议

1. **初学者**：先掌握 ⭐⭐⭐ 级别的组件
2. **进阶开发**：熟悉 ⭐⭐ 级别的组件
3. **高级开发**：了解 ⭐ 级别的组件以备特殊需求

这个表格基本覆盖了 Flutter 官方提供的所有常用组件，是开发 Flutter 应用的完整参考指南！