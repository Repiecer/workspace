import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# 1. 读取并处理Excel数据
def read_excel_data(file_path):
    """
    读取全年12个月的污染物数据
    """
    # 读取Excel文件
    df_raw = pd.read_excel(file_path, header=None)
    
    # 污染物列表（从第3行开始）
    pollutants = df_raw.iloc[2:, 0].dropna().tolist()
    
    # 月份列表
    months = ['1月', '2月', '3月', '4月', '5月', '6月', 
              '7月', '8月', '9月', '10月', '11月', '12月']
    
    # 存储所有数据
    all_data = []
    
    # 处理每个污染物
    for i, pollutant in enumerate(pollutants):
        row_idx = i + 2  # Excel行索引（从0开始，第3行是第一个污染物）
        
        for month_idx, month in enumerate(months):
            # 每个月有4列数据：浓度、流量、运行时间、排放量
            col_offset = month_idx * 4 + 1
            
            # 读取数据
            concentration = df_raw.iloc[row_idx, col_offset]
            flow = df_raw.iloc[row_idx, col_offset + 1]
            days = df_raw.iloc[row_idx, col_offset + 2]
            
            # 计算排放量（如果公式无法读取，则手动计算）
            try:
                emission = df_raw.iloc[row_idx, col_offset + 3]
                if pd.isna(emission):
                    emission = concentration * flow * days / 1000000
            except:
                emission = concentration * flow * days / 1000000
            
            # 添加到数据列表
            all_data.append({
                '污染物': pollutant,
                '月份': month,
                '浓度(mg/L)': float(concentration) if pd.notna(concentration) else 0,
                '流量(m³/d)': float(flow) if pd.notna(flow) else 0,
                '运行时间(d)': float(days) if pd.notna(days) else 0,
                '排放量(t)': float(emission) if pd.notna(emission) else 0
            })
    
    return pd.DataFrame(all_data)

# 2. 创建年度分析仪表板
def create_annual_dashboard(df):
    """
    创建年度污染物分析仪表板
    """
    # 创建子图
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('污染物年度排放量排行', '月度排放量趋势',
                       '污染物浓度分布', '月度排放量对比'),
        specs=[[{'type': 'bar'}, {'type': 'scatter'}],
               [{'type': 'box'}, {'type': 'bar'}]],
        vertical_spacing=0.15,
        horizontal_spacing=0.15
    )
    
    # 子图1：污染物年度排放量排行
    annual_emissions = df.groupby('污染物')['排放量(t)'].sum().reset_index()
    annual_emissions = annual_emissions.sort_values('排放量(t)', ascending=False)
    
    fig.add_trace(
        go.Bar(
            x=annual_emissions['污染物'],
            y=annual_emissions['排放量(t)'],
            name='年度排放量',
            marker_color='steelblue',
            hovertemplate='%{x}<br>排放量: %{y:.6f}t<extra></extra>'
        ),
        row=1, col=1
    )
    
    # 子图2：月度排放量趋势（前5种污染物）
    top_5_pollutants = annual_emissions.head(5)['污染物'].tolist()
    
    for pollutant in top_5_pollutants:
        pollutant_data = df[df['污染物'] == pollutant].copy()
        # 按月份排序
        month_order = {f'{i}月': i for i in range(1, 13)}
        pollutant_data['month_order'] = pollutant_data['月份'].map(month_order)
        pollutant_data = pollutant_data.sort_values('month_order')
        
        fig.add_trace(
            go.Scatter(
                x=pollutant_data['月份'],
                y=pollutant_data['排放量(t)'],
                mode='lines+markers',
                name=pollutant,
                hovertemplate=f'{pollutant}<br>%{{x}}: %{{y:.6f}}t<extra></extra>'
            ),
            row=1, col=2
        )
    
    # 子图3：污染物浓度分布箱型图
    # 取1月份数据
    jan_data = df[df['月份'] == '1月']
    
    fig.add_trace(
        go.Box(
            y=jan_data['浓度(mg/L)'],
            x=jan_data['污染物'],
            name='浓度分布',
            boxpoints='all',
            marker_color='lightseagreen',
            hovertemplate='%{x}<br>浓度: %{y}mg/L<extra></extra>'
        ),
        row=2, col=1
    )
    
    # 子图4：月度总排放量对比
    monthly_totals = df.groupby('月份')['排放量(t)'].sum().reset_index()
    monthly_totals['month_order'] = monthly_totals['月份'].map({f'{i}月': i for i in range(1, 13)})
    monthly_totals = monthly_totals.sort_values('month_order')
    
    fig.add_trace(
        go.Bar(
            x=monthly_totals['月份'],
            y=monthly_totals['排放量(t)'],
            name='月度总排放',
            marker_color='indianred',
            hovertemplate='%{x}<br>总排放: %{y:.6f}t<extra></extra>'
        ),
        row=2, col=2
    )
    
    # 更新布局
    fig.update_layout(
        title_text='2025年度污染物排放分析报告',
        height=900,
        showlegend=True,
        hovermode='closest',
        template='plotly_white'
    )
    
    # 更新坐标轴
    fig.update_xaxes(title_text="污染物", row=1, col=1, tickangle=45)
    fig.update_yaxes(title_text="排放量(t)", row=1, col=1)
    
    fig.update_xaxes(title_text="月份", row=1, col=2)
    fig.update_yaxes(title_text="排放量(t)", row=1, col=2)
    
    fig.update_xaxes(title_text="污染物", row=2, col=1, tickangle=45)
    fig.update_yaxes(title_text="浓度(mg/L)", row=2, col=1)
    
    fig.update_xaxes(title_text="月份", row=2, col=2)
    fig.update_yaxes(title_text="总排放量(t)", row=2, col=2)
    
    return fig

# 3. 创建月度详情图表
def create_monthly_details(df):
    """
    创建月度详情图表，可查看每个月的详细数据
    """
    # 创建下拉菜单选择月份
    months = sorted(df['月份'].unique())
    
    fig = go.Figure()
    
    # 初始显示1月数据
    month_data = df[df['月份'] == '1月']
    
    fig.add_trace(go.Bar(
        x=month_data['污染物'],
        y=month_data['排放量(t)'],
        name='排放量(t)',
        marker_color='royalblue',
        hovertemplate='%{x}<br>排放量: %{y:.6f}t<extra></extra>'
    ))
    
    # 添加浓度数据（右侧Y轴）
    fig.add_trace(go.Scatter(
        x=month_data['污染物'],
        y=month_data['浓度(mg/L)'],
        name='浓度(mg/L)',
        mode='markers+lines',
        marker=dict(size=10, color='crimson'),
        yaxis='y2',
        hovertemplate='%{x}<br>浓度: %{y}mg/L<extra></extra>'
    ))
    
    # 创建下拉菜单
    buttons = []
    for month in months:
        button = dict(
            label=month,
            method="update",
            args=[{"visible": [True, True]},
                  {"title": f"{month}污染物排放详情",
                   "xaxis": {"title": "污染物"},
                   "yaxis": {"title": "排放量(t)"},
                   "yaxis2": {"title": "浓度(mg/L)", "overlaying": "y", "side": "right"}}]
        )
        buttons.append(button)
    
    fig.update_layout(
        title_text='1月污染物排放详情',
        xaxis_title="污染物",
        yaxis_title="排放量(t)",
        yaxis2=dict(
            title="浓度(mg/L)",
            overlaying="y",
            side="right"
        ),
        updatemenus=[dict(
            buttons=buttons,
            direction="down",
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.15,
            yanchor="top"
        )],
        showlegend=True
    )
    
    return fig

# 4. 创建污染物趋势分析
def create_pollutant_trends(df):
    """
    创建污染物趋势分析热力图
    """
    # 创建排放量热力图数据
    heatmap_data = df.pivot_table(
        index='污染物',
        columns='月份',
        values='排放量(t)',
        aggfunc='sum'
    )
    
    # 确保月份顺序
    month_order = [f'{i}月' for i in range(1, 13)]
    heatmap_data = heatmap_data.reindex(columns=month_order)
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Viridis',
        hoverongaps=False,
        hovertemplate='污染物: %{y}<br>月份: %{x}<br>排放量: %{z:.6f}t<extra></extra>'
    ))
    
    fig.update_layout(
        title_text='污染物排放量月度热力图',
        xaxis_title="月份",
        yaxis_title="污染物",
        height=500
    )
    
    return fig

# 5. 生成完整HTML报告
def generate_html_report(file_path, output_file='污染物排放年度报告.html'):
    """
    生成完整的HTML报告
    """
    try:
        print("正在读取数据...")
        df = read_excel_data(file_path)
        
        print("正在创建图表...")
        dashboard_fig = create_annual_dashboard(df)
        monthly_fig = create_monthly_details(df)
        heatmap_fig = create_pollutant_trends(df)
        
        # 创建数据摘要表格
        summary_table = df.pivot_table(
            index='污染物',
            columns='月份',
            values='排放量(t)',
            aggfunc='sum'
        ).round(6)
        
        # 添加年度合计
        summary_table['年度合计'] = summary_table.sum(axis=1)
        
        # 生成HTML
        html_content = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>2025年度污染物排放报告</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 20px; background: #f8f9fa; }}
                .container {{ max-width: 1400px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; padding-bottom: 20px; border-bottom: 2px solid #007bff; margin-bottom: 30px; }}
                .section {{ margin: 30px 0; padding: 20px; border: 1px solid #dee2e6; border-radius: 8px; background: #fff; }}
                .section-title {{ font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 15px; }}
                .data-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 12px; }}
                .data-table th, .data-table td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
                .data-table th {{ background: #007bff; color: white; }}
                .data-table tr:nth-child(even) {{ background: #f8f9fa; }}
                .data-table tr:hover {{ background: #e9ecef; }}
                .note {{ color: #6c757d; font-size: 12px; margin-top: 10px; padding: 10px; background: #f8f9fa; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>2025年度污染物排放分析报告</h1>
                    <p>数据来源: {file_path} | 生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div class="section">
                    <div class="section-title">📊 年度数据分析仪表板</div>
                    <div id="dashboard"></div>
                </div>
                
                <div class="section">
                    <div class="section-title">📅 月度排放详情</div>
                    <p class="note">使用图表左上方的下拉菜单切换不同月份</p>
                    <div id="monthly"></div>
                </div>
                
                <div class="section">
                    <div class="section-title">🔥 排放量热力图</div>
                    <div id="heatmap"></div>
                </div>
                
                <div class="section">
                    <div class="section-title">📋 污染物排放数据总表（单位：吨）</div>
                    <div style="overflow-x: auto;">
                        {summary_table.to_html(classes='data-table')}
                    </div>
                </div>
                
                <div class="note">
                    <p>📌 使用说明：</p>
                    <ul>
                        <li>悬停鼠标查看详细数据</li>
                        <li>使用图表右上角工具栏进行缩放、保存等操作</li>
                        <li>点击图例可显示/隐藏数据系列</li>
                        <li>表格支持水平滚动查看全部数据</li>
                    </ul>
                    <p>📊 数据统计：共分析 {len(df['污染物'].unique())} 种污染物，{len(df['月份'].unique())} 个月份</p>
                </div>
            </div>
            
            <script>
                Plotly.newPlot('dashboard', {dashboard_fig.to_json()});
                Plotly.newPlot('monthly', {monthly_fig.to_json()});
                Plotly.newPlot('heatmap', {heatmap_fig.to_json()});
            </script>
        </body>
        </html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n✅ 报告已生成: {output_file}")
        print(f"📊 污染物数量: {len(df['污染物'].unique())}")
        print(f"📅 月份数量: {len(df['月份'].unique())}")
        print(f"📈 图表数量: 3个")
        
        return output_file
        
    except Exception as e:
        print(f"❌ 生成报告时出错: {e}")
        return None

# 主程序
if __name__ == "__main__":
    # 文件路径
    file_path = "2025ALL.xlsx"
    
    print("=" * 50)
    print("2025年度污染物排放数据分析系统")
    print("=" * 50)
    
    # 生成报告
    output_file = generate_html_report(file_path)
    
    if output_file:
        print(f"\n🎉 报告生成成功！")
        print(f"请用浏览器打开 {output_file} 查看完整报告")
    else:
        print("⚠️  报告生成失败，请检查文件格式和路径")