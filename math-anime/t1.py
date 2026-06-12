from manim import *
import numpy as np

class Problem1_VectorsCoplanar(ThreeDScene):
    """第1题：证明向量a,b,c共面"""
    def construct(self):
        # 标题
        title = Text("第1题：证明向量共面", font_size=42, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(2)

        # 已知条件
        condition = MathTex(
            r"\vec{a}\times\vec{b}+\vec{b}\times\vec{c}+\vec{c}\times\vec{a}=\vec{0}",
            font_size=40
        )
        condition.next_to(title, DOWN, buff=0.8)
        self.play(Write(condition))
        self.wait(3)

        # 步骤1：等式两边点乘 c
        step1 = MathTex(
            r"(\vec{a}\times\vec{b}+\vec{b}\times\vec{c}+\vec{c}\times\vec{a})\cdot\vec{c}=0",
            font_size=38
        )
        step1.next_to(condition, DOWN, buff=0.8)
        self.play(Write(step1))
        self.wait(2)

        # 步骤2：展开点乘
        step2 = MathTex(
            r"(\vec{a}\times\vec{b})\cdot\vec{c}+(\vec{b}\times\vec{c})\cdot\vec{c}+(\vec{c}\times\vec{a})\cdot\vec{c}=0",
            font_size=36
        )
        step2.next_to(step1, DOWN, buff=0.6)
        self.play(Write(step2))
        self.wait(2)

        # 步骤3：说明后两项为零
        step3 = MathTex(
            r"\because (\vec{b}\times\vec{c})\cdot\vec{c}=0,\quad (\vec{c}\times\vec{a})\cdot\vec{c}=0",
            font_size=36
        )
        step3.next_to(step2, DOWN, buff=0.6)
        self.play(Write(step3))
        self.wait(2)

        # 步骤4：得到混合积为零
        step4 = MathTex(
            r"\therefore (\vec{a}\times\vec{b})\cdot\vec{c}=0",
            font_size=40,
            color=YELLOW
        )
        step4.next_to(step3, DOWN, buff=0.6)
        self.play(Write(step4))
        self.wait(3)

        # 结论
        conclusion = Text(
            "混合积为零 ⇒ 三向量共面",
            font_size=38,
            color=GREEN
        )
        conclusion.next_to(step4, DOWN, buff=0.8)
        self.play(Write(conclusion))
        self.wait(4)

        # 三维向量示意图
        axes = ThreeDAxes(
            x_range=[-2, 3, 1],
            y_range=[-2, 3, 1],
            z_range=[-2, 3, 1],
            x_length=5,
            y_length=5,
            z_length=5
        )
        axes.center()
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        self.move_camera(zoom=0.7)
        self.play(Create(axes), run_time=1.5)

        # 定义向量终点（共面示例）
        a_end = np.array([2, 1, 0.5])
        b_end = np.array([1, 2, 0.3])
        c_end = np.array([1.5, 1.2, 0.8])

        vec_a = Arrow3D(start=ORIGIN, end=a_end, color=RED, thickness=0.05)
        vec_b = Arrow3D(start=ORIGIN, end=b_end, color=GREEN, thickness=0.05)
        vec_c = Arrow3D(start=ORIGIN, end=c_end, color=BLUE, thickness=0.05)

        label_a = Text("a", color=RED).next_to(vec_a.get_end(), UR, buff=0.1)
        label_b = Text("b", color=GREEN).next_to(vec_b.get_end(), UL, buff=0.1)
        label_c = Text("c", color=BLUE).next_to(vec_c.get_end(), UR, buff=0.1)

        self.play(Create(vec_a), Create(vec_b), Create(vec_c))
        self.play(Write(label_a), Write(label_b), Write(label_c))
        self.wait(3)

        # 辅助平面（通过三个终点确定一个平面）
        points = [a_end, b_end, c_end]
        # 计算平面法向量
        normal = np.cross(b_end - a_end, c_end - a_end)
        normal = normal / np.linalg.norm(normal)
        # 创建平面（简化：画一个半透明的矩形）
        plane_center = (a_end + b_end + c_end) / 3
        plane = Square(side_length=3, color=BLUE, fill_opacity=0.3, fill_color=BLUE)
        plane.move_to(plane_center)
        plane.rotate(np.arccos(np.dot(normal, np.array([0,0,1]))), axis=np.cross(normal, np.array([0,0,1])))
        self.play(FadeIn(plane, scale=0.5))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.wait(4)

class Problem2_PerpendicularLine(ThreeDScene):
    """第2题：求与L1, L2都垂直相交的直线方程"""
    def construct(self):
        title = Text("第2题：求与 L₁, L₂ 垂直相交的直线", font_size=40, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(2)

        # 直线方程
        l1 = MathTex(r"L_1: \frac{x-1}{1}=\frac{y}{2}=\frac{z}{-1}", font_size=38)
        l2 = MathTex(r"L_2: \frac{x}{2}=\frac{y-1}{1}=\frac{z+1}{1}", font_size=38)
        l1.next_to(title, DOWN, buff=0.5)
        l2.next_to(l1, DOWN, buff=0.3)
        self.play(Write(l1), Write(l2))
        self.wait(2)

        # 方向向量
        d1 = MathTex(r"\vec{d}_1 = (1,2,-1)", font_size=38)
        d2 = MathTex(r"\vec{d}_2 = (2,1,1)", font_size=38)
        d1.next_to(l2, DOWN, buff=0.5)
        d2.next_to(d1, DOWN, buff=0.3)
        self.play(Write(d1), Write(d2))
        self.wait(2)

        # 公垂线方向向量 = d1 × d2
        cross_title = Text("公垂线方向向量 = d₁ × d₂", font_size=34, color=YELLOW)
        cross_title.next_to(d2, DOWN, buff=0.6)
        self.play(Write(cross_title))
        self.wait(1)

        cross_step = MathTex(
            r"\vec{d} = \vec{d}_1 \times \vec{d}_2 = \begin{vmatrix} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ 1 & 2 & -1 \\ 2 & 1 & 1 \end{vmatrix}",
            font_size=38
        )
        cross_step.next_to(cross_title, DOWN, buff=0.5)
        self.play(Write(cross_step))
        self.wait(2)

        calc = MathTex(
            r"= (2\cdot1 - (-1)\cdot1,\; (-1)\cdot2 - 1\cdot1,\; 1\cdot1 - 2\cdot2)",
            font_size=36
        )
        calc.next_to(cross_step, DOWN, buff=0.5)
        self.play(Write(calc))
        self.wait(2)

        d_vec = MathTex(
            r"= (3,\; -3,\; -3) \parallel (1,\,-1,\,-1)",
            font_size=38,
            color=GREEN
        )
        d_vec.next_to(calc, DOWN, buff=0.5)
        self.play(Write(d_vec))
        self.wait(3)

        # 求交点参数
        param_title = Text("设 L₁ 上点 P₁(1+t, 2t, -t),  L₂ 上点 P₂(2s, 1+s, -1+s)", font_size=32)
        param_title.next_to(d_vec, DOWN, buff=0.8)
        self.play(Write(param_title))
        self.wait(2)

        cond = MathTex(r"\overrightarrow{P_1P_2} \parallel \vec{d} \quad \Rightarrow \quad \frac{2s-(1+t)}{1} = \frac{(1+s)-2t}{-1} = \frac{(-1+s)-(-t)}{-1}", font_size=32)
        cond.next_to(param_title, DOWN, buff=0.5)
        self.play(Write(cond))
        self.wait(3)

        solve = MathTex(r"\text{解得 } t=1,\; s=0", font_size=36, color=YELLOW)
        solve.next_to(cond, DOWN, buff=0.6)
        self.play(Write(solve))
        self.wait(2)

        point1 = MathTex(r"P_1(2,2,-1),\quad P_2(0,1,-1)", font_size=34)
        point1.next_to(solve, DOWN, buff=0.5)
        self.play(Write(point1))
        self.wait(2)

        # 直线方程
        line_eq = MathTex(
            r"\text{所求直线: } \frac{x-2}{1} = \frac{y-2}{-1} = \frac{z+1}{-1}",
            font_size=38,
            color=GREEN
        )
        line_eq.next_to(point1, DOWN, buff=0.6)
        self.play(Write(line_eq))
        self.wait(4)

        # 3D 图形展示
        axes = ThreeDAxes(
            x_range=[-2, 4, 1],
            y_range=[-2, 4, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=5
        )
        axes.center()
        self.set_camera_orientation(phi=65*DEGREES, theta=-50*DEGREES)
        self.move_camera(zoom=0.8)
        self.play(Create(axes), run_time=1.5)

        # 绘制 L1 直线
        t_vals = np.linspace(-1, 2, 20)
        pts1 = [np.array([1+t, 2*t, -t]) for t in t_vals]
        line1 = VMobject(color=RED)
        line1.set_points_as_corners(pts1)
        # 绘制 L2 直线
        s_vals = np.linspace(-1, 2, 20)
        pts2 = [np.array([2*s, 1+s, -1+s]) for s in s_vals]
        line2 = VMobject(color=BLUE)
        line2.set_points_as_corners(pts2)
        self.play(Create(line1), Create(line2))
        self.wait(2)

        # 绘制公垂线
        p1 = np.array([2,2,-1])
        p2 = np.array([0,1,-1])
        common_line = Line3D(start=p1, end=p2, color=GREEN, thickness=0.06)
        self.play(Create(common_line))
        self.wait(2)

        # 添加标注
        label_l1 = Text("L₁", color=RED, font_size=28).next_to(pts1[-1], UR, buff=0.2)
        label_l2 = Text("L₂", color=BLUE, font_size=28).next_to(pts2[-1], DR, buff=0.2)
        label_line = Text("所求直线", color=GREEN, font_size=28).next_to(common_line.get_center(), DL, buff=0.3)
        self.play(Write(label_l1), Write(label_l2), Write(label_line))
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(6)
        self.stop_ambient_camera_rotation()
        self.wait(4)