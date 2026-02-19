import os
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import (
    Bar, Line, Pie, Scatter, Grid, Page, Tab, Timeline, 
    Radar, HeatMap, Boxplot, Sankey, WordCloud, Funnel
)
import warnings
import re
import glob
from datetime import datetime
import math
warnings.filterwarnings('ignore')

class RobustDataExtractor:
    """健壮版数据提取器"""
    
    def __init__(self):
        self.water_data = []
        self.exhaust_data = []
        
    def extract_all_data(self):
        """提取所有数据"""
        print("🔍 开始提取数据...")
        
        # 查找所有Excel文件
        excel_files = []
        for ext in ['*.xlsx', '*.xls']:
            excel_files.extend(glob.glob(ext))
        
        if not excel_files:
            print("⚠️  未找到Excel文件")
            return False
        
        print(f"找到 {len(excel_files)} 个Excel文件")
        
        # 处理每个文件
        for file in excel_files:
            print(f"  处理: {os.path.basename(file)}")
            try:
                self.process_file(file)
            except Exception as e:
                print(f"  处理失败: {str(e)}")
                continue
        
        print(f"\n📊 数据提取完成:")
        print(f"  废水数据: {len(self.water_data)} 条")
        print(f"  废气数据: {len(self.exhaust_data)} 条")
        
        return True
    
    def process_file(self, filepath):
        """处理单个文件"""
        # 从文件名提取年份和季度
        year, quarter = self.extract_year_quarter(filepath)
        
        # 读取Excel文件
        xls = pd.ExcelFile(filepath)
        
        # 处理每个sheet
        for sheet_name in xls.sheet_names:
            try:
                df = pd.read_excel(filepath, sheet_name=sheet_name, header=None)
                
                # 根据sheet名判断类型
                if '废水' in sheet_name or '污水' in sheet_name or 'water' in sheet_name.lower():
                    self.extract_water_data(df, year, quarter, filepath)
                elif '废气' in sheet_name or 'exhaust' in sheet_name.lower():
                    self.extract_exhaust_data(df, year, quarter, filepath)
                else:
                    # 尝试自动识别
                    self.auto_extract_data(df, year, quarter, filepath, sheet_name)
                    
            except Exception as e:
                continue
    
    def extract_year_quarter(self, filename):
        """从文件名提取年份和季度"""
        filename = os.path.basename(filename)
        
        # 尝试提取年份
        year = 2023
        year_match = re.search(r'(\d{4})', filename)
        if year_match:
            year = int(year_match.group(1))
        
        # 尝试提取季度
        quarter = 1
        quarter_match = re.search(r'[第\s]?(\d)[季季度Q]', filename)
        if quarter_match:
            quarter = int(quarter_match.group(1))
        
        return year, quarter
    
    def auto_extract_data(self, df, year, quarter, filepath, sheet_name):
        """自动识别并提取数据"""
        # 将DataFrame转为字符串进行检查
        df_str = df.head(20).to_string()
        
        # 检查是否包含废水相关关键词
        water_keywords = ['COD', '氨氮', '总氮', '总磷', '浓度mg/L', '流量m³/d']
        exhaust_keywords = ['颗粒物', 'NOX', 'SO2', 'VOC', '浓度mg/m³', '排气量']
        
        water_count = sum(1 for kw in water_keywords if kw in df_str)
        exhaust_count = sum(1 for kw in exhaust_keywords if kw in df_str)
        
        if water_count > exhaust_count:
            self.extract_water_data(df, year, quarter, filepath)
        elif exhaust_count > 0:
            self.extract_exhaust_data(df, year, quarter, filepath)
    
    def extract_water_data(self, df, year, quarter, filepath):
        """提取废水数据"""
        try:
            # 查找数据开始行
            start_row = self.find_water_start_row(df)
            if start_row is None:
                return
            
            # 季度对应的月份
            months = self.get_months_for_quarter(quarter)
            
            # 查找污染物列
            pollutant_col = None
            for col in range(min(10, df.shape[1])):
                if start_row < len(df) and col < df.shape[1]:
                    cell_val = str(df.iloc[start_row, col])
                    if 'COD' in cell_val or '氨氮' in cell_val:
                        pollutant_col = col
                        break
            
            if pollutant_col is None:
                pollutant_col = 0
            
            # 提取污染物名称
            pollutants = []
            row = start_row
            while row < min(start_row + 20, len(df)):
                if pollutant_col < df.shape[1]:
                    pollutant = df.iloc[row, pollutant_col]
                    if pd.notna(pollutant) and str(pollutant).strip():
                        clean_pollutant = str(pollutant).strip()
                        if any(kw in clean_pollutant for kw in ['COD', '氨氮', '总氮', '总磷', '悬浮物', '石油类']):
                            pollutants.append(clean_pollutant)
                row += 1
            
            if not pollutants:
                pollutants = ['COD', '氨氮', '六价铬', '石油类', '悬浮物', '氟化物', 
                            '铅', '镍', '铬', 'BOD5', '总氮', '总磷']
            
            # 提取每月数据
            for month_idx, month_num in enumerate(months):
                month_name = f"{month_num}月"
                base_col = pollutant_col + 1 + month_idx * 4
                
                for poll_idx, pollutant in enumerate(pollutants):
                    data_row = start_row + poll_idx
                    if data_row >= len(df) or base_col + 3 >= df.shape[1]:
                        continue
                    
                    try:
                        # 读取数据
                        conc = self.safe_get_value(df, data_row, base_col, 0)
                        flow = self.safe_get_value(df, data_row, base_col + 1, 0)
                        days = self.safe_get_value(df, data_row, base_col + 2, 0)
                        
                        # 计算或读取排放量
                        emission = self.safe_get_value(df, data_row, base_col + 3, conc * flow * days / 1000000)
                        
                        # 添加到数据
                        self.water_data.append({
                            '年份': year,
                            '季度': quarter,
                            '月份': month_name,
                            '月份数值': month_num,
                            '污染物': pollutant,
                            '浓度(mg/L)': float(conc),
                            '流量(m³/d)': float(flow),
                            '运行时间(d)': float(days),
                            '排放量(t)': float(emission) if not pd.isna(emission) else 0,
                            '文件': os.path.basename(filepath),
                            '类型': '废水'
                        })
                        
                    except Exception as e:
                        continue
                        
        except Exception as e:
            print(f"  提取废水数据出错: {e}")
    
    def extract_exhaust_data(self, df, year, quarter, filepath):
        """提取废气数据"""
        try:
            # 查找数据开始行
            start_row = self.find_exhaust_start_row(df)
            if start_row is None:
                return
            
            # 季度对应的月份
            months = self.get_months_for_quarter(quarter)
            
            # 查找关键列
            source_col = None
            pollutant_col = None
            
            for col in range(min(10, df.shape[1])):
                if start_row > 0 and col < df.shape[1]:
                    cell_val = str(df.iloc[start_row-1, col])
                    if '排放口' in cell_val:
                        source_col = col
                    elif '污染物' in cell_val:
                        pollutant_col = col
            
            if pollutant_col is None:
                pollutant_col = 1 if source_col == 0 else 0
            
            if source_col is None:
                source_col = 0
            
            # 提取数据行
            data_rows = []
            row = start_row
            
            while row < min(start_row + 50, len(df)):
                if pollutant_col < df.shape[1]:
                    pollutant = df.iloc[row, pollutant_col]
                    source = df.iloc[row, source_col] if source_col < df.shape[1] else '未知'
                    
                    if pd.notna(pollutant) and str(pollutant).strip():
                        poll_str = str(pollutant).strip()
                        if any(kw in poll_str for kw in ['颗粒物', 'NOX', 'SO2', 'VOC', '氟化物', '氯化氢']):
                            data_rows.append({
                                'row': row,
                                '污染物': poll_str,
                                '排放口': str(source).strip() if pd.notna(source) else '未知'
                            })
                
                row += 1
            
            # 提取每月数据
            for month_idx, month_num in enumerate(months):
                month_name = f"{month_num}月"
                base_col = max(source_col, pollutant_col) + 2 + month_idx * 4
                
                for data_row in data_rows:
                    row_idx = data_row['row']
                    
                    if row_idx >= len(df) or base_col + 3 >= df.shape[1]:
                        continue
                    
                    try:
                        # 读取数据
                        conc = self.safe_get_value(df, row_idx, base_col, 0)
                        flow = self.safe_get_value(df, row_idx, base_col + 1, 0)
                        hours = self.safe_get_value(df, row_idx, base_col + 2, 0)
                        
                        # 计算或读取排放量（废气除以10^9）
                        emission = self.safe_get_value(df, row_idx, base_col + 3, 
                                                      conc * flow * hours / 1000000000)
                        
                        # 添加到数据
                        self.exhaust_data.append({
                            '年份': year,
                            '季度': quarter,
                            '月份': month_name,
                            '月份数值': month_num,
                            '排放口': data_row['排放口'],
                            '污染物': data_row['污染物'],
                            '浓度(mg/m³)': float(conc),
                            '排气量(m³/h)': float(flow),
                            '运行时间(h)': float(hours),
                            '排放量(t)': float(emission) if not pd.isna(emission) else 0,
                            '文件': os.path.basename(filepath),
                            '类型': '废气'
                        })
                        
                    except Exception as e:
                        continue
                        
        except Exception as e:
            print(f"  提取废气数据出错: {e}")
    
    def find_water_start_row(self, df):
        """查找废水数据开始行"""
        for i in range(min(30, len(df))):
            for j in range(min(10, df.shape[1])):
                if j < df.shape[1]:
                    cell_val = str(df.iloc[i, j])
                    if 'COD' in cell_val or '氨氮' in cell_val or '浓度mg/L' in cell_val:
                        return i
        return 2  # 默认从第2行开始
    
    def find_exhaust_start_row(self, df):
        """查找废气数据开始行"""
        for i in range(min(30, len(df))):
            for j in range(min(10, df.shape[1])):
                if j < df.shape[1]:
                    cell_val = str(df.iloc[i, j])
                    if '颗粒物' in cell_val or 'NOX' in cell_val or '浓度mg/m³' in cell_val:
                        return i
        return 3  # 默认从第3行开始
    
    def get_months_for_quarter(self, quarter):
        """获取季度对应的月份"""
        if quarter == 1:
            return [1, 2, 3]
        elif quarter == 2:
            return [4, 5, 6]
        elif quarter == 3:
            return [7, 8, 9]
        else:
            return [10, 11, 12]
    
    def safe_get_value(self, df, row, col, default):
        """安全获取单元格值"""
        try:
            if row < len(df) and col < df.shape[1]:
                value = df.iloc[row, col]
                if pd.isna(value):
                    return default
                try:
                    return float(value)
                except:
                    return default
        except:
            pass
        return default
    
    def get_dataframes(self):
        """返回DataFrame"""
        water_df = pd.DataFrame(self.water_data) if self.water_data else pd.DataFrame()
        exhaust_df = pd.DataFrame(self.exhaust_data) if self.exhaust_data else pd.DataFrame()
        
        # 添加衍生字段
        if not water_df.empty:
            water_df['季节'] = water_df['季度'].map({1: '春季', 2: '夏季', 3: '秋季', 4: '冬季'})
            water_df['年度季度'] = water_df['年份'].astype(str) + 'Q' + water_df['季度'].astype(str)
        
        if not exhaust_df.empty:
            exhaust_df['季节'] = exhaust_df['季度'].map({1: '春季', 2: '夏季', 3: '秋季', 4: '冬季'})
            exhaust_df['年度季度'] = exhaust_df['年份'].astype(str) + 'Q' + exhaust_df['季度'].astype(str)
        
        return water_df, exhaust_df

class ComprehensiveVisualizer:
    """综合可视化器 - 修复版"""
    
    def __init__(self, water_df, exhaust_df):
        self.water_df = water_df
        self.exhaust_df = exhaust_df
    
    # ============ 1. 基础趋势图 ============
    def create_basic_trend_chart(self):
        """创建基础趋势图"""
        if self.water_df.empty and self.exhaust_df.empty:
            return None
        
        line = Line(init_opts=opts.InitOpts(width="1400px", height="600px"))
        
        # 创建时间序列
        if not self.water_df.empty:
            # 按月份汇总废水数据
            water_monthly = self.water_df.groupby('月份数值')['排放量(t)'].sum().reset_index()
            water_monthly = water_monthly.sort_values('月份数值')
            
            months = [f"{int(m)}月" for m in water_monthly['月份数值'].tolist()]
            line.add_xaxis(months)
            line.add_yaxis(
                "废水排放",
                [round(x, 6) for x in water_monthly['排放量(t)'].tolist()],
                is_smooth=True,
                symbol_size=8,
                label_opts=opts.LabelOpts(is_show=False),
                itemstyle_opts=opts.ItemStyleOpts(color="#5470c6"),
                linestyle_opts=opts.LineStyleOpts(width=3)
            )
        
        if not self.exhaust_df.empty:
            # 按月份汇总废气数据
            exhaust_monthly = self.exhaust_df.groupby('月份数值')['排放量(t)'].sum().reset_index()
            exhaust_monthly = exhaust_monthly.sort_values('月份数值')
            
            if 'months' not in locals():
                months = [f"{int(m)}月" for m in exhaust_monthly['月份数值'].tolist()]
                line.add_xaxis(months)
            
            line.add_yaxis(
                "废气排放",
                [round(x, 6) for x in exhaust_monthly['排放量(t)'].tolist()],
                is_smooth=True,
                symbol_size=8,
                label_opts=opts.LabelOpts(is_show=False),
                itemstyle_opts=opts.ItemStyleOpts(color="#ee6666"),
                linestyle_opts=opts.LineStyleOpts(width=3, type_='dashed')
            )
        
        line.set_global_opts(
            title_opts=opts.TitleOpts(title="废水废气排放趋势"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            xaxis_opts=opts.AxisOpts(
                name="月份",
                axislabel_opts=opts.LabelOpts(rotate=45)
            ),
            yaxis_opts=opts.AxisOpts(
                name="排放量(t)",
                axislabel_opts=opts.LabelOpts(formatter="{value} t")
            ),
            legend_opts=opts.LegendOpts(pos_top="10%"),
            toolbox_opts=opts.ToolboxOpts(
                is_show=True,
                feature={
                    "saveAsImage": {"title": "保存图片"},
                    "restore": {"title": "还原"},
                    "dataView": {"title": "数据视图"},
                    "dataZoom": {"title": "区域缩放"},
                }
            ),
            datazoom_opts=[opts.DataZoomOpts()]
        )
        
        return line
    
    # ============ 2. 污染物排行图 ============
    def create_pollutant_ranking(self):
        """创建污染物排行榜"""
        if self.water_df.empty:
            return None
        
        # 计算污染物总排放量
        pollutant_totals = self.water_df.groupby('污染物')['排放量(t)'].sum().reset_index()
        pollutant_totals = pollutant_totals.sort_values('排放量(t)', ascending=True)
        
        # 只显示前10种
        top_pollutants = pollutant_totals.tail(10)
        
        bar = Bar(init_opts=opts.InitOpts(width="1000px", height="500px"))
        
        bar.add_xaxis(top_pollutants['污染物'].tolist())
        bar.add_yaxis(
            "排放量(t)",
            [round(x, 6) for x in top_pollutants['排放量(t)'].tolist()],
            label_opts=opts.LabelOpts(
                position="right",
                formatter="{c} t"
            ),
            itemstyle_opts=opts.ItemStyleOpts(color="#91cc75")
        )
        bar.reversal_axis()
        
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="废水主要污染物排行榜"),
            xaxis_opts=opts.AxisOpts(
                name="排放量(t)",
                axislabel_opts=opts.LabelOpts(formatter="{value} t")
            ),
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(font_size=12)
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="shadow",
                formatter="{b}: {c} t"
            )
        )
        
        return bar
    
    # ============ 3. 季度对比图 ============
    def create_quarterly_comparison(self):
        """创建季度对比图"""
        if self.water_df.empty and self.exhaust_df.empty:
            return None
        
        # 按季度汇总数据
        quarterly_data = []
        
        if not self.water_df.empty:
            water_quarterly = self.water_df.groupby(['年份', '季度'])['排放量(t)'].sum().reset_index()
            water_quarterly['类型'] = '废水'
            quarterly_data.append(water_quarterly)
        
        if not self.exhaust_df.empty:
            exhaust_quarterly = self.exhaust_df.groupby(['年份', '季度'])['排放量(t)'].sum().reset_index()
            exhaust_quarterly['类型'] = '废气'
            quarterly_data.append(exhaust_quarterly)
        
        if not quarterly_data:
            return None
        
        quarterly_df = pd.concat(quarterly_data, ignore_index=True)
        quarterly_df = quarterly_df.sort_values(['年份', '季度'])
        
        # 创建季度标签
        quarterly_df['季度标签'] = quarterly_df['年份'].astype(str) + '年Q' + quarterly_df['季度'].astype(str)
        
        bar = Bar(init_opts=opts.InitOpts(width="1200px", height="500px"))
        
        quarters = quarterly_df['季度标签'].unique().tolist()
        bar.add_xaxis(quarters)
        
        # 添加废水数据
        if not self.water_df.empty:
            water_values = []
            for quarter in quarters:
                val = quarterly_df[(quarterly_df['季度标签'] == quarter) & 
                                   (quarterly_df['类型'] == '废水')]['排放量(t)']
                water_values.append(round(val.iloc[0], 6) if not val.empty else 0)
            
            bar.add_yaxis(
                "废水",
                water_values,
                label_opts=opts.LabelOpts(is_show=False),
                itemstyle_opts=opts.ItemStyleOpts(color="#5470c6")
            )
        
        # 添加废气数据
        if not self.exhaust_df.empty:
            exhaust_values = []
            for quarter in quarters:
                val = quarterly_df[(quarterly_df['季度标签'] == quarter) & 
                                   (quarterly_df['类型'] == '废气')]['排放量(t)']
                exhaust_values.append(round(val.iloc[0], 6) if not val.empty else 0)
            
            bar.add_yaxis(
                "废气",
                exhaust_values,
                label_opts=opts.LabelOpts(is_show=False),
                itemstyle_opts=opts.ItemStyleOpts(color="#ee6666")
            )
        
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="季度排放量对比"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(rotate=45)
            ),
            yaxis_opts=opts.AxisOpts(
                name="排放量(t)",
                axislabel_opts=opts.LabelOpts(formatter="{value} t")
            ),
            legend_opts=opts.LegendOpts(pos_top="10%")
        )
        
        return bar
    
    # ============ 4. 浓度分布图 ============
    def create_concentration_distribution(self):
        """创建浓度分布图"""
        if self.water_df.empty:
            return None
        
        # 选取前8种污染物
        top_pollutants = self.water_df.groupby('污染物')['排放量(t)'].sum().nlargest(8).index.tolist()
        
        scatter = Scatter(init_opts=opts.InitOpts(width="1200px", height="500px"))
        
        colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', 
                 '#73c0de', '#3ba272', '#fc8452', '#9a60b4']
        
        for idx, pollutant in enumerate(top_pollutants):
            pollutant_data = self.water_df[self.water_df['污染物'] == pollutant]
            
            if not pollutant_data.empty:
                scatter.add_xaxis(pollutant_data['浓度(mg/L)'].tolist())
                scatter.add_yaxis(
                    pollutant,
                    [round(x, 6) for x in pollutant_data['排放量(t)'].tolist()],
                    symbol_size=10,
                    label_opts=opts.LabelOpts(is_show=False),
                    itemstyle_opts=opts.ItemStyleOpts(color=colors[idx % len(colors)], opacity=0.6)
                )
        
        scatter.set_global_opts(
            title_opts=opts.TitleOpts(title="污染物浓度与排放量关系"),
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
                formatter="浓度: {c0} mg/L<br/>排放量: {c1} t"
            ),
            xaxis_opts=opts.AxisOpts(
                name="浓度(mg/L)",
                type_="value"
            ),
            yaxis_opts=opts.AxisOpts(
                name="排放量(t)",
                axislabel_opts=opts.LabelOpts(formatter="{value} t")
            ),
            legend_opts=opts.LegendOpts(pos_top="10%")
        )
        
        return scatter
    
    # ============ 5. 热力图分析 ============
    def create_heatmap_analysis(self):
        """创建热力图"""
        if self.water_df.empty:
            return None
        
        try:
            # 按月份和污染物创建数据
            pivot_data = self.water_df.pivot_table(
                index='污染物',
                columns='月份数值',
                values='排放量(t)',
                aggfunc='sum',
                fill_value=0
            ).round(6)
            
            # 只保留有数据的污染物和月份
            pivot_data = pivot_data.loc[(pivot_data > 0).any(axis=1)]
            pivot_data = pivot_data.loc[:, (pivot_data > 0).any(axis=0)]
            
            if pivot_data.empty:
                return None
            
            # 准备热力图数据
            data = []
            months = pivot_data.columns.tolist()
            pollutants = pivot_data.index.tolist()
            
            for i, pollutant in enumerate(pollutants):
                for j, month in enumerate(months):
                    value = pivot_data.loc[pollutant, month]
                    if value > 0:
                        data.append([j, i, value])
            
            heatmap = HeatMap(init_opts=opts.InitOpts(width="1200px", height="600px"))
            
            heatmap.add_xaxis([f'{int(m)}月' for m in months])
            heatmap.add_yaxis(
                "排放量(t)",
                pollutants,
                data,
                label_opts=opts.LabelOpts(is_show=False),
            )
            
            heatmap.set_global_opts(
                title_opts=opts.TitleOpts(title="污染物排放月度热力图"),
                tooltip_opts=opts.TooltipOpts(
                    formatter="月份: {b}<br/>污染物: {a}<br/>排放量: {c} t"
                ),
                xaxis_opts=opts.AxisOpts(
                    name="月份",
                    type_="category",
                    axislabel_opts=opts.LabelOpts(rotate=45)
                ),
                yaxis_opts=opts.AxisOpts(
                    name="污染物",
                    type_="category"
                ),
                visualmap_opts=opts.VisualMapOpts(
                    min_=0,
                    max_=float(pivot_data.values.max()) if not pivot_data.empty else 0,
                    is_calculable=True,
                    orient="vertical",
                    pos_left="0%",
                    pos_top="middle"
                ),
            )
            
            return heatmap
            
        except Exception as e:
            print(f"创建热力图时出错: {e}")
            return None
    
    # ============ 6. 饼图分析 ============
    def create_pie_chart(self):
        """创建饼图"""
        if self.water_df.empty:
            return None
        
        try:
            # 计算污染物占比
            pollutant_totals = self.water_df.groupby('污染物')['排放量(t)'].sum().reset_index()
            pollutant_totals = pollutant_totals.sort_values('排放量(t)', ascending=False)
            
            # 只显示前8种，其余归为"其他"
            top_n = 8
            if len(pollutant_totals) > top_n:
                top_pollutants = pollutant_totals.head(top_n)
                other_total = pollutant_totals.iloc[top_n:]['排放量(t)'].sum()
                
                data = []
                for _, row in top_pollutants.iterrows():
                    data.append((row['污染物'], round(row['排放量(t)'], 6)))
                
                if other_total > 0:
                    data.append(("其他", round(other_total, 6)))
            else:
                data = [(row['污染物'], round(row['排放量(t)'], 6)) 
                       for _, row in pollutant_totals.iterrows()]
            
            pie = Pie(init_opts=opts.InitOpts(width="800px", height="500px"))
            
            pie.add(
                "",
                data,
                radius=["30%", "75%"],
                label_opts=opts.LabelOpts(
                    formatter="{b}: {c}t ({d}%)"
                )
            )
            
            pie.set_global_opts(
                title_opts=opts.TitleOpts(title="污染物排放占比"),
                tooltip_opts=opts.TooltipOpts(
                    trigger="item",
                    formatter="{a}<br/>{b}: {c}t ({d}%)"
                ),
                legend_opts=opts.LegendOpts(
                    orient="vertical",
                    pos_left="left",
                    type_="scroll"
                )
            )
            
            return pie
            
        except Exception as e:
            print(f"创建饼图时出错: {e}")
            return None
    
    # ============ 7. 箱型图分析 ============
    def create_box_plot(self):
        """创建箱型图"""
        if self.water_df.empty:
            return None
        
        try:
            # 选取前10种污染物
            top_pollutants = self.water_df.groupby('污染物')['排放量(t)'].sum().nlargest(10).index.tolist()
            
            # 准备数据
            x_data = []
            y_data = []
            
            for pollutant in top_pollutants:
                concentrations = self.water_df[self.water_df['污染物'] == pollutant]['浓度(mg/L)']
                concentrations = concentrations[concentrations > 0].tolist()
                
                if concentrations:
                    x_data.append(pollutant)
                    y_data.append(concentrations)
            
            if not x_data:
                return None
            
            boxplot = Boxplot(init_opts=opts.InitOpts(width="1200px", height="500px"))
            
            boxplot.add_xaxis(x_data)
            boxplot.add_yaxis(
                "浓度分布",
                boxplot.prepare_data(y_data),
                tooltip_opts=opts.TooltipOpts(
                    formatter="污染物: {b}<br/>浓度范围: {c}"
                ),
                itemstyle_opts=opts.ItemStyleOpts(color="#73c0de")
            )
            
            boxplot.set_global_opts(
                title_opts=opts.TitleOpts(title="污染物浓度分布箱型图"),
                xaxis_opts=opts.AxisOpts(
                    name="污染物",
                    axislabel_opts=opts.LabelOpts(rotate=45)
                ),
                yaxis_opts=opts.AxisOpts(
                    name="浓度(mg/L)",
                    splitarea_opts=opts.SplitAreaOpts(is_show=True)
                )
            )
            
            return boxplot
            
        except Exception as e:
            print(f"创建箱型图时出错: {e}")
            return None
    
    # ============ 8. 雷达图分析 ============
    def create_radar_chart(self):
        """创建雷达图"""
        if self.water_df.empty:
            return None
        
        try:
            # 选取前6种污染物
            top_pollutants = self.water_df.groupby('污染物')['排放量(t)'].sum().nlargest(6).index.tolist()
            
            radar = Radar(init_opts=opts.InitOpts(width="800px", height="600px"))
            
            # 创建schema
            schema = []
            max_values = []
            
            for pollutant in top_pollutants:
                max_emission = self.water_df[self.water_df['污染物'] == pollutant]['排放量(t)'].max()
                schema.append(opts.RadarIndicatorItem(name=pollutant, max_=float(max_emission * 1.2)))
                max_values.append(float(max_emission))
            
            radar.add_schema(schema=schema, splitarea_opt=opts.SplitAreaOpts(is_show=True))
            
            # 添加数据
            data_values = []
            for pollutant in top_pollutants:
                total_emission = self.water_df[self.water_df['污染物'] == pollutant]['排放量(t)'].sum()
                data_values.append(float(total_emission))
            
            radar.add(
                series_name="排放量",
                data=[data_values],
                color="#5470c6",
                areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
                linestyle_opts=opts.LineStyleOpts(width=2)
            )
            
            radar.set_global_opts(
                title_opts=opts.TitleOpts(title="主要污染物排放对比雷达图"),
                legend_opts=opts.LegendOpts(is_show=False)
            )
            
            return radar
            
        except Exception as e:
            print(f"创建雷达图时出错: {e}")
            return None
    
    # ============ 9. 词云图 ============
    def create_wordcloud(self):
        """创建词云图"""
        if self.water_df.empty and self.exhaust_df.empty:
            return None
        
        try:
            # 合并污染物数据
            word_data = []
            
            if not self.water_df.empty:
                water_words = self.water_df.groupby('污染物')['排放量(t)'].sum().reset_index()
                for _, row in water_words.iterrows():
                    weight = int(row['排放量(t)'] * 1000)
                    if weight > 0:
                        word_data.append((row['污染物'], weight))
            
            if not self.exhaust_df.empty:
                exhaust_words = self.exhaust_df.groupby('污染物')['排放量(t)'].sum().reset_index()
                for _, row in exhaust_words.iterrows():
                    weight = int(row['排放量(t)'] * 1000)
                    if weight > 0:
                        word_data.append((row['污染物'], weight))
            
            if not word_data:
                return None
            
            wordcloud = WordCloud(init_opts=opts.InitOpts(width="1000px", height="600px"))
            
            wordcloud.add(
                series_name="污染物",
                data_pair=word_data,
                word_size_range=[20, 100],
                shape="circle",
                tooltip_opts=opts.TooltipOpts(
                    formatter="{b}: 权重{c}"
                )
            )
            
            wordcloud.set_global_opts(
                title_opts=opts.TitleOpts(
                    title="污染物排放权重词云图",
                    title_textstyle_opts=opts.TextStyleOpts(font_size=23)
                )
            )
            
            return wordcloud
            
        except Exception as e:
            print(f"创建词云图时出错: {e}")
            return None
    
    # ============ 10. 漏斗图 ============
    def create_funnel_chart(self):
        """创建漏斗图"""
        if self.water_df.empty:
            return None
        
        try:
            # 计算污染物排放占比
            pollutant_totals = self.water_df.groupby('污染物')['排放量(t)'].sum().reset_index()
            pollutant_totals = pollutant_totals.sort_values('排放量(t)', ascending=False)
            
            # 只显示前8种
            top_pollutants = pollutant_totals.head(8)
            total_emission = top_pollutants['排放量(t)'].sum()
            
            funnel = Funnel(init_opts=opts.InitOpts(width="800px", height="500px"))
            
            data = []
            for _, row in top_pollutants.iterrows():
                percentage = round(row['排放量(t)'] / total_emission * 100, 2)
                data.append([row['污染物'], percentage])
            
            funnel.add(
                series_name="排放占比",
                data_pair=data,
                gap=2,
                tooltip_opts=opts.TooltipOpts(
                    formatter="{a}<br/>{b}: {c}%"
                ),
                label_opts=opts.LabelOpts(position="inside"),
                itemstyle_opts=opts.ItemStyleOpts(border_color="#fff", border_width=1),
            )
            
            funnel.set_global_opts(
                title_opts=opts.TitleOpts(title="主要污染物排放占比漏斗图"),
                tooltip_opts=opts.TooltipOpts(trigger="item")
            )
            
            return funnel
            
        except Exception as e:
            print(f"创建漏斗图时出错: {e}")
            return None

def create_html_report(water_df, exhaust_df, visualizer):
    """创建HTML报告"""
    
    try:
        tab = Tab(page_title="废水废气排放分析报告")
        
        # 1. 趋势分析
        trend_chart = visualizer.create_basic_trend_chart()
        if trend_chart:
            tab.add(trend_chart, "排放趋势")
        
        # 2. 污染物分析
        ranking_chart = visualizer.create_pollutant_ranking()
        if ranking_chart:
            tab.add(ranking_chart, "污染物排行")
        
        # 3. 季度对比
        quarterly_chart = visualizer.create_quarterly_comparison()
        if quarterly_chart:
            tab.add(quarterly_chart, "季度对比")
        
        # 4. 浓度分析
        concentration_chart = visualizer.create_concentration_distribution()
        if concentration_chart:
            tab.add(concentration_chart, "浓度关系")
        
        # 5. 热力图
        heatmap_chart = visualizer.create_heatmap_analysis()
        if heatmap_chart:
            tab.add(heatmap_chart, "热力图")
        
        # 6. 占比分析
        pie_chart = visualizer.create_pie_chart()
        if pie_chart:
            tab.add(pie_chart, "排放占比")
        
        # 7. 分布分析
        box_chart = visualizer.create_box_plot()
        if box_chart:
            tab.add(box_chart, "浓度分布")
        
        # 8. 雷达图
        radar_chart = visualizer.create_radar_chart()
        if radar_chart:
            tab.add(radar_chart, "雷达图")
        
        # 9. 词云图
        wordcloud_chart = visualizer.create_wordcloud()
        if wordcloud_chart:
            tab.add(wordcloud_chart, "词云图")
        
        # 10. 漏斗图
        funnel_chart = visualizer.create_funnel_chart()
        if funnel_chart:
            tab.add(funnel_chart, "漏斗图")
        
        # 生成报告
        output_file = "废水废气排放分析报告.html"
        tab.render(output_file)
        
        # 美化报告
        beautify_report(output_file, water_df, exhaust_df)
        
        return output_file
        
    except Exception as e:
        print(f"生成HTML报告时出错: {e}")
        return None

def beautify_report(filename, water_df, exhaust_df):
    """美化报告"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 添加CSS样式
        css_style = """
        <style>
            body {
                font-family: 'Microsoft YaHei', Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background: #f5f7fa;
                color: #333;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 20px rgba(0,0,0,0.1);
            }
            
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 3px solid #007bff;
            }
            
            .header h1 {
                color: #2c3e50;
                margin-bottom: 10px;
            }
            
            .summary-cards {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                margin: 30px 0;
            }
            
            .card {
                flex: 1;
                min-width: 200px;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: center;
            }
            
            .card.water {
                border-top: 4px solid #5470c6;
            }
            
            .card.exhaust {
                border-top: 4px solid #ee6666;
            }
            
            .card.total {
                border-top: 4px solid #91cc75;
            }
            
            .card-value {
                font-size: 24px;
                font-weight: bold;
                margin: 10px 0;
            }
            
            .card-label {
                color: #666;
                font-size: 14px;
            }
            
            .data-section {
                margin: 40px 0;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
            }
            
            .section-title {
                font-size: 18px;
                color: #2c3e50;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #dee2e6;
            }
            
            .table-container {
                overflow-x: auto;
                margin: 20px 0;
            }
            
            .data-table {
                width: 100%;
                border-collapse: collapse;
                font-size: 12px;
            }
            
            .data-table th, .data-table td {
                border: 1px solid #ddd;
                padding: 8px 12px;
                text-align: center;
            }
            
            .data-table th {
                background: #007bff;
                color: white;
                font-weight: bold;
            }
            
            .data-table tr:nth-child(even) {
                background-color: #f8f9fa;
            }
            
            .data-table tr:hover {
                background-color: #e9ecef;
            }
            
            .chart-container {
                margin: 20px 0;
                padding: 20px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 1px 5px rgba(0,0,0,0.05);
            }
            
            .footer {
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #dee2e6;
                color: #666;
                font-size: 12px;
            }
        </style>
        """
        
        # 创建数据概览卡片
        water_total = water_df['排放量(t)'].sum() if not water_df.empty else 0
        exhaust_total = exhaust_df['排放量(t)'].sum() if not exhaust_df.empty else 0
        total_emission = water_total + exhaust_total
        
        summary_cards = f"""
        <div class="summary-cards">
            <div class="card water">
                <div class="card-label">废水总排放</div>
                <div class="card-value">{water_total:.6f} t</div>
                <div class="card-label">{len(water_df)} 条记录</div>
            </div>
            
            <div class="card exhaust">
                <div class="card-label">废气总排放</div>
                <div class="card-value">{exhaust_total:.6f} t</div>
                <div class="card-label">{len(exhaust_df)} 条记录</div>
            </div>
            
            <div class="card total">
                <div class="card-label">总排放量</div>
                <div class="card-value">{total_emission:.6f} t</div>
                <div class="card-label">综合统计</div>
            </div>
        </div>
        """
        
        # 插入自定义内容
        content = content.replace('</head>', css_style + '</head>')
        
        # 找到第一个图表div并插入概览内容
        chart_marker = '<div id="'
        if chart_marker in content:
            parts = content.split(chart_marker, 1)
            content = parts[0] + summary_cards + '<div class="chart-container">' + chart_marker + parts[1]
        else:
            content = content.replace('<body>', '<body>' + summary_cards)
        
        # 添加页脚
        footer = f"""
        <div class="footer">
            <p>📈 报告生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
            <p>🔍 包含 {len(water_df['污染物'].unique() if not water_df.empty else 0)} 种废水污染物分析</p>
            <p>📊 10类可视化图表，全方位展示排放特征</p>
            <p>© 环境数据分析系统</p>
        </div>
        """
        content = content.replace('</body>', footer + '</body>')
        
        # 添加容器
        content = content.replace('<body>', '<body><div class="container">')
        content = content.replace('</body>', '</div></body>')
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 报告美化完成")
        
    except Exception as e:
        print(f"⚠️  美化报告时出错: {e}")

def main():
    print("=" * 60)
    print("🏭 废水废气排放数据分析系统")
    print("=" * 60)
    
    # 数据提取
    print("\n🔍 开始提取数据...")
    extractor = RobustDataExtractor()
    
    if not extractor.extract_all_data():
        print("❌ 数据提取失败")
        return
    
    water_df, exhaust_df = extractor.get_dataframes()
    
    if water_df.empty and exhaust_df.empty:
        print("❌ 未提取到有效数据")
        return
    
    print(f"\n📊 数据准备完成:")
    print(f"  废水数据: {len(water_df)} 条记录")
    print(f"  废气数据: {len(exhaust_df)} 条记录")
    
    # 创建可视化
    print("\n🎨 正在创建可视化图表...")
    visualizer = ComprehensiveVisualizer(water_df, exhaust_df)
    
    # 生成报告
    print("📄 正在生成分析报告...")
    output_file = create_html_report(water_df, exhaust_df, visualizer)
    
    if output_file:
        print(f"\n🎉 报告生成完成！")
        print(f"📁 报告文件: {output_file}")
        
        print(f"\n📋 报告包含内容:")
        charts = [
            "排放趋势图", "污染物排行榜", "季度对比图", "浓度关系图",
            "热力图分析", "排放占比图", "浓度分布图", "雷达对比图",
            "词云展示图", "漏斗分析图"
        ]
        for i, chart in enumerate(charts, 1):
            print(f"  {i:2d}. {chart}")
        
        print(f"\n💡 使用说明:")
        print(f"  1. 用浏览器打开 {output_file}")
        print(f"  2. 点击顶部标签页切换不同图表")
        print(f"  3. 鼠标悬停查看详细数据")
        print(f"  4. 使用工具栏进行缩放、保存等操作")
        print(f"  5. 报告完全离线可用，无需联网")
    else:
        print("❌ 生成报告失败")

if __name__ == "__main__":
    main()