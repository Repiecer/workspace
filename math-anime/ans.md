### 第7章 空间解析几何与向量代数

**题目1**  
设向量 \(\vec{a},\vec{b},\vec{c}\) 满足 \(\vec{a}\times\vec{b}+\vec{b}\times\vec{c}+\vec{c}\times\vec{a}=\vec{0}\)。证明：\(\vec{a},\vec{b},\vec{c}\) 共面。

**解法一（混合积）**  
将等式两边点乘 \(\vec{c}\)：  
\((\vec{a}\times\vec{b})\cdot\vec{c}+(\vec{b}\times\vec{c})\cdot\vec{c}+(\vec{c}\times\vec{a})\cdot\vec{c}=0\)。  
由于 \((\vec{b}\times\vec{c})\cdot\vec{c}=0\)，\((\vec{c}\times\vec{a})\cdot\vec{c}=0\)，得 \((\vec{a}\times\vec{b})\cdot\vec{c}=0\)，即混合积为零，故三向量共面。

**解法二（反证法）**  
若 \(\vec{a},\vec{b},\vec{c}\) 不共面，则它们线性无关，可作基。设 \(\vec{a}\times\vec{b}\) 垂直于 \(\vec{a},\vec{b}\) 所在平面，而 \(\vec{b}\times\vec{c}\) 垂直于 \(\vec{b},\vec{c}\) 所在平面，两方向不同，其和不可能为 \(\vec{0}\) 除非系数为零，矛盾。

---

**题目2**  
已知直线 \(L_1: \frac{x-1}{1}=\frac{y}{2}=\frac{z}{-1}\)，\(L_2: \frac{x}{2}=\frac{y-1}{1}=\frac{z+1}{1}\)。求与 \(L_1,L_2\) 都垂直相交的直线方程。

**解法一（方向向量+参数）**  
\(L_1\) 方向 \(\vec{s}_1=(1,2,-1)\)，\(L_2\) 方向 \(\vec{s}_2=(2,1,1)\)。所求直线方向 \(\vec{s}=\vec{s}_1\times\vec{s}_2=(3,-3,-3)\parallel(1,-1,-1)\)。  
设 \(L_1\) 上点 \(A(1+t,2t,-t)\)，\(L_2\) 上点 \(B(2s,1+s,-1+s)\)，\(\overrightarrow{AB}=(2s-t-1,\;1+s-2t,\;-1+s+t)\)。  
由 \(\overrightarrow{AB}\parallel\vec{s}=(1,-1,-1)\) 得 \(\frac{2s-t-1}{1}=\frac{1+s-2t}{-1}=\frac{-1+s+t}{-1}=\lambda\)。  
解得 \(t=\frac{2}{3}, s=\frac{4}{3}, \lambda=-\frac{1}{3}\)，得 \(A(\frac{5}{3},\frac{4}{3},-\frac{2}{3})\)，直线方程：\(\frac{x-5/3}{1}=\frac{y-4/3}{-1}=\frac{z+2/3}{-1}\)。

**解法二（公垂线公式）**  
公垂线方向 \(\vec{s}=\vec{s}_1\times\vec{s}_2\)，再求两点连线垂直于 \(\vec{s}_1,\vec{s}_2\) 的条件，联立解交点，结果同上。

---

### 第8章 多元函数微分法及其应用

**题目3**  
设 \(z=f(xy, x^2-y^2)\)，\(f\) 二阶连续偏导。求 \(\frac{\partial^2 z}{\partial x\partial y}\)。

**解法一（链式法则直接求导）**  
令 \(u=xy,\;v=x^2-y^2\)，则 \(z_x = f_u\cdot y + f_v\cdot 2x\)。  
对 \(y\) 求导：  
\[
z_{xy}= \frac{\partial}{\partial y}(f_u y) + \frac{\partial}{\partial y}(f_v\cdot 2x)=f_u + y(f_{uu}\cdot x + f_{uv}\cdot (-2y)) + 2x(f_{vu}\cdot x + f_{vv}\cdot (-2y)).
\]  
由 \(f_{uv}=f_{vu}\) 得：
\[
z_{xy}=f_u + xy f_{uu} - 2y^2 f_{uv} + 2x^2 f_{uv} - 4xy f_{vv}=f_u + xy f_{uu} + 2(x^2-y^2)f_{uv} - 4xy f_{vv}.
\]

**解法二（先 \(y\) 后 \(x\) 对称性）**  
\(z_y = f_u\cdot x + f_v\cdot (-2y)\)，再对 \(x\) 求导可得相同结果，体现对称性。

---

**题目4**  
设 \(u(x,y)\) 满足 \(u_x + u_y = 0\)，且 \(u(x,0)=\sin x\)。求 \(u(x,y)\)。

**解法一（特征线法）**  
特征方程 \(\frac{dx}{1}=\frac{dy}{1}=\frac{du}{0}\)，得 \(x-y=C\)，且 \(u\) 沿特征线为常数，故 \(u(x,y)=f(x-y)\)。由 \(u(x,0)=f(x)=\sin x\)，得 \(u(x,y)=\sin(x-y)\)。

**解法二（变量变换）**  
令 \(\xi=x-y,\;\eta=x+y\)，则 \(u_x=u_\xi+u_\eta,\;u_y=-u_\xi+u_\eta\)，代入得 \(2u_\eta=0\)，故 \(u=\varphi(\xi)=\varphi(x-y)\)，再由初值得 \(\varphi=\sin\)。

**解法三（常数变易法）**  
视为关于 \(x\) 的方程：\(u_x=-u_y\)，对 \(y\) 积分得 \(u(x,y)=\int -u_y dy\)，不如前两法直接。

---

**题目5**  
求曲面 \(z=e^{x}\sin y\) 在点 \((0,\frac{\pi}{2},1)\) 处的切平面与 \(xOy\) 面的夹角。

**解法一（法向量夹角）**  
\(z_x=e^x\sin y,\;z_y=e^x\cos y\)，在点 \((0,\pi/2,1)\) 处，\(z_x=1,\;z_y=0\)，切平面法向量 \(\vec{n}=(z_x,z_y,-1)=(1,0,-1)\)。\(xOy\) 面法向量 \(\vec{m}=(0,0,1)\)。夹角 \(\theta\) 满足 \(\cos\theta=\frac{|\vec{n}\cdot\vec{m}|}{\|\vec{n}\|\|\vec{m}\|}=\frac{1}{\sqrt{2}}\)，故 \(\theta=\frac{\pi}{4}\)。

**解法二（切平面方程求夹角）**  
切平面方程：\(z-1=1\cdot(x-0)+0\cdot(y-\pi/2)\)，即 \(z=x+1\)，其法向量 \((1,0,-1)\)，同上。

---

### 第9章 重积分

**题目6**  
计算 \(\iint_D \frac{dxdy}{(1+x^2+y^2)^{3/2}}\)，\(D: x^2+y^2\le 1\)。

**解法一（极坐标）**  
\[
\int_0^{2\pi}d\theta\int_0^1\frac{r\,dr}{(1+r^2)^{3/2}}=2\pi\left[-\frac{1}{\sqrt{1+r^2}}\right]_0^1=2\pi\left(1-\frac{1}{\sqrt{2}}\right).
\]

**解法二（广义极坐标换元）**  
令 \(u=r^2\)，则 \(\int_0^1\frac{r\,dr}{(1+r^2)^{3/2}}=\frac12\int_0^1(1+u)^{-3/2}du=\left[-(1+u)^{-1/2}\right]_0^1=1-\frac{1}{\sqrt{2}}\)，再乘 \(2\pi\)。

---

**题目7**  
计算 \(\iiint_V (x^2+y^2) dV\)，\(V: x^2+y^2+z^2\le R^2\)。

**解法一（对称性+球坐标）**  
由对称性，\(\iiint x^2 dV = \iiint y^2 dV = \iiint z^2 dV = \frac13\iiint (x^2+y^2+z^2)dV\)。  
球坐标：\(\iiint r^2 dV = \int_0^R r^2\cdot 4\pi r^2 dr = 4\pi \frac{R^5}{5}\)。所以 \(\iiint x^2 dV = \frac{4\pi R^5}{15}\)，故 \(\iiint (x^2+y^2)dV = \frac{8\pi R^5}{15}\)。

**解法二（柱坐标直接积分）**  
\[
\int_0^{2\pi}d\theta\int_{-R}^R dz\int_0^{\sqrt{R^2-z^2}} r^2 \cdot r dr = 2\pi\int_{-R}^R \frac{(R^2-z^2)^2}{4} dz = \frac{\pi}{2}\int_{-R}^R (R^4 -2R^2z^2+z^4)dz = \frac{8\pi R^5}{15}.
\]

---

### 第10章 曲线积分与曲面积分

**题目8**  
计算 \(\int_L (x^2+y^2) ds\)，\(L: x^2+y^2=ax\) (\(a>0\))。

**解法一（利用曲线方程）**  
在 \(L\) 上 \(x^2+y^2=ax\)，积分化为 \(\int_L ax\, ds\)。圆周圆心 \((\frac{a}{2},0)\)，半径 \(\frac{a}{2}\)，由对称性 \(\int_L x\, ds = \frac{a}{2}\cdot 2\pi\cdot\frac{a}{2} = \frac{\pi a^2}{2}\)，故原积分 \(=a\cdot\frac{\pi a^2}{2}=\frac{\pi a^3}{2}\)。

**解法二（参数化）**  
令 \(x=\frac{a}{2}+\frac{a}{2}\cos\theta,\;y=\frac{a}{2}\sin\theta\)，\(\theta\in[0,2\pi]\)，\(ds=\frac{a}{2}d\theta\)，\(x^2+y^2=ax=\frac{a^2}{2}(1+\cos\theta)\)，积分得 \(\frac{\pi a^3}{2}\)。

---

**题目9**  
\(\int_L (y^2 dx + x^2 dy)\)，\(L\)：椭圆 \(\frac{x^2}{a^2}+\frac{y^2}{b^2}=1\) 逆时针。

**解法一（格林公式）**  
\(P=y^2,\;Q=x^2\)，\(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}=2x-2y\)。积分 \(=\iint_D (2x-2y)dxdy\)，由对称性 \(=0\)。

**解法二（参数化）**  
\(x=a\cos t,\;y=b\sin t\)，\(dx=-a\sin t dt,\;dy=b\cos t dt\)，被积式化为 \(b^2\sin^2 t\cdot(-a\sin t)+a^2\cos^2 t\cdot(b\cos t)\)，周期积分结果为0。

---

**题目10**  
\(\iint_{\Sigma} (x+y+z)dS\)，\(\Sigma\)：平面 \(x+y+z=1\) 被柱面 \(x^2+y^2\le 1\) 所截部分。

**解法一（利用曲面方程）**  
在 \(\Sigma\) 上 \(x+y+z=1\)，故被积函数为1，积分 \(=\iint_{\Sigma} dS = \text{曲面面积}\)。投影 \(D: x^2+y^2\le1\)，平面与 \(xOy\) 面夹角余弦 \(\cos\gamma = \frac{1}{\sqrt{3}}\)，面积 \(=\frac{|D|}{\cos\gamma}=\frac{\pi}{1/\sqrt{3}}=\sqrt{3}\pi\)。

**解法二（投影法直接算）**  
\(z=1-x-y\)，\(dS=\sqrt{1+z_x^2+z_y^2}dxdy=\sqrt{3}dxdy\)，积分 \(=\iint_D 1\cdot\sqrt{3}dxdy=\sqrt{3}\pi\)。

---

**题目11**  
用高斯公式计算 \(\iint_{\Sigma} x^3 dy dz + y^3 dz dx + z^3 dx dy\)，\(\Sigma\)：球面 \(x^2+y^2+z^2=R^2\) 外侧。

**解法一（散度定理）**  
散度 \(\nabla\cdot\vec{F}=3x^2+3y^2+3z^2=3r^2\)。积分 \(=\iiint_V 3r^2 dV = 3\int_0^R r^2\cdot 4\pi r^2 dr = 12\pi\cdot\frac{R^5}{5}=\frac{12\pi R^5}{5}\)。

**解法二（直接积分对称性）**  
由对称性 \(\iint_{\Sigma} x^3 dy dz = \iint_{\Sigma} y^3 dz dx = \iint_{\Sigma} z^3 dx dy\)，且等于 \(\frac13\iint_{\Sigma} (x^3 dy dz+\cdots)\)，再利用高斯公式简化，结果同上。

---

### 第11章 无穷级数

**题目12**  
判断 \(\sum_{n=1}^{\infty} \frac{\ln n}{n^{3/2}}\) 敛散性。

**解法一（比较判别法）**  
对 \(\forall\varepsilon>0\)，当 \(n\) 充分大时 \(\ln n < n^{\varepsilon}\)，取 \(\varepsilon=1/4\)，则 \(\frac{\ln n}{n^{3/2}} < \frac{n^{1/4}}{n^{3/2}}=\frac{1}{n^{5/4}}\)，\(\sum 1/n^{5/4}\) 收敛，故原级数收敛。

**解法二（积分判别法）**  
考虑 \(\int_2^{\infty} \frac{\ln x}{x^{3/2}}dx\)，令 \(t=\ln x\) 或分部积分得收敛。

---

**题目13**  
求幂级数 \(\sum_{n=0}^{\infty} \frac{x^{2n}}{(2n)!}\) 的和函数。

**解法一（已知展开式）**  
\(\cosh x = \frac{e^x+e^{-x}}{2} = \sum_{n=0}^{\infty} \frac{x^{2n}}{(2n)!}\)，故和函数为 \(\cosh x\)。

**解法二（微分方程）**  
设 \(S(x)=\sum \frac{x^{2n}}{(2n)!}\)，则 \(S''(x)=S(x)\)，\(S(0)=1,S'(0)=0\)，解 \(S(x)=C_1 e^x+C_2 e^{-x}\) 代入得 \(C_1=C_2=1/2\)，即 \(\cosh x\)。

---

**题目14**  
将 \(f(x)=\arctan x\) 展开为幂级数，并求 \(\sum_{n=0}^{\infty} \frac{(-1)^n}{2n+1}\)。

**解法一（逐项积分）**  
\(\arctan x = \int_0^x \frac{dt}{1+t^2} = \int_0^x \sum_{n=0}^{\infty} (-1)^n t^{2n} dt = \sum_{n=0}^{\infty} (-1)^n \frac{x^{2n+1}}{2n+1}\)，收敛域 \(|x|\le 1\)。令 \(x=1\) 得 \(\frac{\pi}{4}=\sum_{n=0}^{\infty} \frac{(-1)^n}{2n+1}\)。

**解法二（复数法）**  
\(\sum_{n=0}^{\infty} \frac{(-1)^n}{2n+1} = \sum_{n=0}^{\infty} \int_0^1 (-1)^n x^{2n} dx = \int_0^1 \frac{dx}{1+x^2}=\frac{\pi}{4}\)。

---

**题目15**  
\(f(x)=x\) 在 \([-\pi,\pi)\) 上周期延拓，求傅里叶级数及 \(\sum 1/n^2\)。

**解法一（傅里叶展开+帕塞瓦尔）**  
\(f\) 奇函数，\(a_n=0\)，\(b_n=\frac{2}{\pi}\int_0^\pi x\sin nx dx = \frac{2(-1)^{n+1}}{n}\)。级数：\(f(x)\sim 2\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}\sin nx\)。  
帕塞瓦尔：\(\frac{1}{\pi}\int_{-\pi}^{\pi}x^2dx = \sum_{n=1}^{\infty} b_n^2\)，左边=\(\frac{2\pi^2}{3}\)，右边=\(\sum_{n=1}^{\infty}\frac{4}{n^2}\)，故 \(\sum_{n=1}^{\infty}\frac{1}{n^2}=\frac{\pi^2}{6}\)。

**解法二（傅里叶级数在 \(x=\pi/2\) 处值）**  
令 \(x=\pi/2\) 得 \(\frac{\pi}{2}=2\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}\sin\frac{n\pi}{2}\)，奇偶项分析得 \(\frac{\pi}{4}=\sum_{k=0}^{\infty}\frac{(-1)^k}{2k+1}\)，不是 \(\sum 1/n^2\)，故仍需帕塞瓦尔。

---

### 综合/提高题

**题目16**  
求极限 \(\lim_{(x,y)\to(0,0)} \frac{x^2 y}{x^4+y^2}\)。

**解法一（不同路径）**  
沿 \(y=x^2\)：\(\frac{x^2\cdot x^2}{x^4+x^4}=\frac{x^4}{2x^4}=\frac12\)。沿 \(y=0\)：极限为0。故极限不存在。

**解法二（极坐标）**  
令 \(x=r\cos\theta,\;y=r\sin\theta\)，则 \(\frac{r^3\cos^2\theta\sin\theta}{r^4\cos^4\theta+r^2\sin^2\theta}=\frac{r\cos^2\theta\sin\theta}{r^2\cos^4\theta+\sin^2\theta}\)，当 \(r\to0\) 时，若 \(\sin\theta\neq0\)，极限为0；若 \(\sin\theta=0\) 则分子为0；但沿 \(\theta\) 使分母中 \(\sin^2\theta\) 占优时，极限依赖于路径，故不存在。

---

**题目17**  
\(\vec{F}=(y,z,x)\)，\(C\)：三角形 \((1,0,0),(0,1,0),(0,0,1)\) 边界，方向从 \(z\) 轴正向看逆时针。求 \(\oint_C\vec{F}\cdot d\vec{r}\)。

**解法一（斯托克斯公式）**  
旋度 \(\nabla\times\vec{F}=(-1,-1,-1)\)，取 \(S\) 为三角形平面 \(x+y+z=1\)，法向量 \(\vec{n}=\frac{(1,1,1)}{\sqrt{3}}\)。  
\(\iint_S (\nabla\times\vec{F})\cdot\vec{n} dS = \iint_S (-1,-1,-1)\cdot\frac{(1,1,1)}{\sqrt{3}} dS = -\sqrt{3}\iint_S dS\)。三角形边长 \(\sqrt{2}\)，面积 \(=\frac{\sqrt{3}}{2}\)，故积分 \(=-\sqrt{3}\cdot\frac{\sqrt{3}}{2}=-\frac{3}{2}\)。

**解法二（直接参数化）**  
将三角形分为三条线段，分别计算线积分，结果相同。

---

**题目18**  
\(f(x,y)=\begin{cases}\frac{x^2 y}{x^2+y^2},&(x,y)\neq0\\0,&(0,0)\end{cases}\)，讨论可微性。

**解法一（定义验证）**  
\(f_x(0,0)=f_y(0,0)=0\)。全增量 \(\Delta f - df = \frac{x^2 y}{x^2+y^2}\)。沿 \(y=x\)：\(\frac{x^3}{2x^2}=\frac{x}{2}\)，与 \(\sqrt{x^2+y^2}\) 的比值为 \(\frac{|x|/2}{\sqrt{2}|x|}=\frac{1}{2\sqrt{2}}\not\to0\)，故不可微。

**解法二（方向导数不线性）**  
沿方向 \((1,1)\) 的方向导数存在但不等于梯度点乘方向（梯度为0，但方向导数为 \(\frac{1}{2\sqrt{2}}\)），故不可微。

---

**题目19**  
曲线 \(L: x=t, y=t^2, z=t^3\) 上点 \((1,1,1)\) 处的切线方程及该点到原点距离。

**解法一（切向量）**  
\(\vec{r}'(t)=(1,2t,3t^2)\)，在 \(t=1\) 处得 \((1,2,3)\)。切线：\(\frac{x-1}{1}=\frac{y-1}{2}=\frac{z-1}{3}\)。点到原点距离 \(=\sqrt{1^2+1^2+1^2}=\sqrt{3}\)。

**解法二（参数式）**  
切线参数方程：\(x=1+s,\;y=1+2s,\;z=1+3s\)，距离由两点距离公式得。

---

**题目20**  
证明 \(\sum_{n=1}^{\infty} \frac{(-1)^n}{\sqrt{n}}\) 条件收敛。

**解法一（莱布尼茨+发散）**  
绝对值 \(\sum 1/\sqrt{n}\) 是 \(p=1/2\) 的 \(p\)-级数，发散。而 \(a_n=1/\sqrt{n}\) 递减趋于0，由莱布尼茨判别法，交错级数收敛，故条件收敛。

**解法二（柯西收敛原理否定绝对收敛，再证收敛）**  
绝对收敛否定：部分和 \(S_{2n}=\sum_{k=1}^{2n}1/\sqrt{k}\) 无界。收敛性：\(|R_n|<\frac{1}{\sqrt{n+1}}\to0\)。