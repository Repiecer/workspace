import os
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie, Grid, Page, Tab, Timeline
import warnings
import re
from datetime import datetime
warnings.filterwarnings('ignore')

class SmartDataExtractor:
    """智能数据提取器，自动识别Excel格式"""
    
    def __init__(self):
        self.water_data = []  # 废水数据
        self.exhaust_data = []  # 废气数据
        
    def find_excel_files(self):
        """智能查找所有Excel文件"""
        excel_files = []
        
        # 方法1：查找所有.xlsx文件
        for file in os.listdir('.'):
            if file.endswith('.xlsx') or file.endswith('.xls'):
                excel_files.append(file)
        
        # 方法2：如果没有找到，查找特定模式的文件
        if not excel_files:
            patterns = [
                '2023年*季度*.xlsx',
                '2024年*季度*.xlsx', 
                '2025年*季度*.xlsx',
                '*废水废气*.xlsx',
                '*排放量*.xlsx'
            ]
            for pattern in patterns:
                files = glob.glob(pattern)
                excel_files.extend(files)
        
        # 去重
        excel_files = list(set(excel_files))
        
        print(f"📂 找到 {len(excel_files)} 个Excel文件")
        for file in excel_files:
            print(f"  - {file}")
        
        return excel_files
    
    def extract_year_quarter_from_filename(self, filename):
        """从文件名中提取年份和季度"""
        try:
            # 尝试多种模式匹配
            patterns = [
                r'(\d{4})年.*?第(\d)季度',  # 2023年第1季度
                r'(\d{4})年.*?Q(\d)',       # 2023年Q1
                r'(\d{4})年.*?(\d)季度',    # 2023年1季度
                r'(\d{4})'                  # 只提取年份
            ]
            
            for pattern in patterns:
                match = re.search(pattern, filename)
                if match:
                    year = int(match.group(1))
                    quarter = int(match.group(2)) if len(match.groups()) > 1 else 1
                    return year, quarter
            
            # 如果都没匹配到，使用默认值
            return 2023, 1
            
        except:
            return 2023, 1
    
    def smart_find_data_start(self, sheet_data, sheet_name):
        """智能查找数据开始位置"""
        # 查找可能的关键词
        keywords = {
            '废水': ['污染物名称', 'COD', '氨氮', '总氮', '排放口', '浓度mg/L'],
            '废气': ['污染物名称', '颗粒物', 'NOX', 'SO2', 'VOC', '浓度mg/m³']
        }
        
        for i in range(min(20, len(sheet_data))):  # 只检查前20行
            row_str = ' '.join([str(x) for x in sheet_data.iloc[i].astype(str).tolist()])
            
            for keyword in keywords.get(sheet_name, keywords['废水']):
                if keyword in row_str:
                    return i
        
        # 如果没有找到关键词，返回默认位置
        return 2 if sheet_name == '废水' else 3
    
    def extract_water_data(self, filepath, sheet_data, year, quarter):
        """提取废水数据（智能适应不同格式）"""
        try:
            # 智能查找数据开始行
            start_row = self.smart_find_data_start(sheet_data, '废水')
            
            # 查找污染物名称所在的列
            pollutant_col = None
            for col in range(min(10, len(sheet_data.columns))):  # 只检查前10列
                if sheet_data.iloc[start_row, col] in ['污染物名称', 'COD', '氨氮', '总氮']:
                    pollutant_col = col
                    break
            
            if pollutant_col is None:
                # 如果没找到，假设是第一列
                pollutant_col = 0
            
            # 提取污染物列表（直到遇到空行或非污染物名称）
            pollutants = []
            row_idx = start_row
            while row_idx < len(sheet_data) and row_idx < start_row + 20:
                pollutant = sheet_data.iloc[row_idx, pollutant_col]
                if pd.isna(pollutant) or pollutant == '':
                    break
                # 只添加真正的污染物名称
                if any(name in str(pollutant) for name in ['COD', '氨氮', '六价铬', '石油类', '悬浮物', 
                                                          '氟化物', '铅', '镍', '铬', 'BOD5', '总氮', '总磷', 'PH']):
                    pollutants.append(str(pollutant).strip())
                row_idx += 1
            
            if not pollutants:
                # 使用默认污染物列表
                pollutants = ['COD', '氨氮', '六价铬', '石油类', '悬浮物', 
                            '氟化物', '铅', '镍', '铬', 'BOD5', '总氮', '总磷', 'PH']
            
            # 处理每个季度的三个月数据
            months = [1, 2, 3] if quarter == 1 else [4, 5, 6] if quarter == 2 else [7, 8, 9] if quarter == 3 else [10, 11, 12]
            
            for month_idx, month in enumerate(months):
                # 智能查找月份数据列（每个月4列：浓度、流量、时间、排放量）
                base_col = None
                
                # 查找月份标题
                for col in range(len(sheet_data.columns)):
                    cell = sheet_data.iloc[start_row-1, col]  # 标题可能在上一行
                    if cell and (f"{month}月" in str(cell) or f"{quarter}季度" in str(cell) or f"第{quarter}季度" in str(cell)):
                        base_col = col
                        break
                
                if base_col is None:
                    # 如果没找到月份标题，尝试根据位置计算
                    base_col = month_idx * 4 + 1
                
                for i, pollutant in enumerate(pollutants):
                    data_row = start_row + i
                    if data_row >= len(sheet_data):
                        continue
                    
                    # 尝试读取数据
                    try:
                        # 浓度
                        conc_col = base_col
                        conc = sheet_data.iloc[data_row, conc_col]
                        if pd.isna(conc):
                            conc = 0
                        
                        # 流量
                        flow_col = base_col + 1
                        flow = sheet_data.iloc[data_row, flow_col] if flow_col < len(sheet_data.columns) else 0
                        if pd.isna(flow):
                            flow = 0
                        
                        # 运行时间
                        time_col = base_col + 2
                        days = sheet_data.iloc[data_row, time_col] if time_col < len(sheet_data.columns) else 0
                        if pd.isna(days):
                            days = 0
                        
                        # 排放量（尝试读取或计算）
                        emission_col = base_col + 3
                        if emission_col < len(sheet_data.columns):
                            emission = sheet_data.iloc[data_row, emission_col]
                            if pd.isna(emission):
                                emission = float(conc) * float(flow) * float(days) / 1000000
                        else:
                            emission = float(conc) * float(flow) * float(days) / 1000000
                        
                        # 添加到数据列表
                        self.water_data.append({
                            '文件': os.path.basename(filepath),
                            '年份': year,
                            '季度': quarter,
                            '月份': f'{month}月',
                            '污染物': pollutant,
                            '浓度(mg/L)': float(conc),
                            '流量(m³/d)': float(flow),
                            '运行时间(d)': float(days),
                            '排放量(t)': float(emission) if not pd.isna(emission) else 0
                        })
                        
                    except Exception as e:
                        # 如果出错，跳过这个污染物
                        continue
            
            return True
            
        except Exception as e:
            print(f"⚠️  提取废水数据时出错（{os.path.basename(filepath)}）：{e}")
            return False
    
    def extract_exhaust_data(self, filepath, sheet_data, year, quarter):
        """提取废气数据（智能适应不同格式）"""
        try:
            # 智能查找数据开始行
            start_row = self.smart_find_data_start(sheet_data, '废气')
            
            # 查找排放口和污染物名称所在的列
            emission_col = None
            pollutant_col = None
            
            for col in range(min(10, len(sheet_data.columns))):
                cell = sheet_data.iloc[start_row, col] if start_row < len(sheet_data) else None
                if cell:
                    cell_str = str(cell)
                    if '排放口' in cell_str:
                        emission_col = col
                    elif '污染物名称' in cell_str or any(name in cell_str for name in ['颗粒物', 'NOX', 'SO2']):
                        pollutant_col = col
            
            if pollutant_col is None:
                pollutant_col = 1 if emission_col == 0 else 0
            
            # 提取数据（直到遇到空行）
            data_rows = []
            row_idx = start_row + 1  # 跳过标题行
            
            while row_idx < len(sheet_data) and row_idx < start_row + 50:  # 最多检查50行
                pollutant = sheet_data.iloc[row_idx, pollutant_col] if pollutant_col < len(sheet_data.columns) else None
                emission_source = sheet_data.iloc[row_idx, emission_col] if emission_col is not None and emission_col < len(sheet_data.columns) else ""
                
                if pd.isna(pollutant) or pollutant == '':
                    row_idx += 1
                    continue
                
                # 只添加真正的污染物数据
                pollutant_str = str(pollutant)
                valid_pollutants = ['颗粒物', 'NOX', 'SO2', 'VOC', '氟化物', '氯化氢', '氮氧化物', '二氧化硫']
                
                if any(vp in pollutant_str for vp in valid_pollutants):
                    data_rows.append({
                        '排放口': str(emission_source) if not pd.isna(emission_source) else "",
                        '污染物': pollutant_str,
                        '行索引': row_idx
                    })
                
                row_idx += 1
            
            if not data_rows:
                # 使用默认数据
                data_rows = [
                    {'排放口': '背层', '污染物': '颗粒物', '行索引': start_row + 1},
                    {'排放口': '面层', '污染物': '颗粒物', '行索引': start_row + 2},
                    {'排放口': '焙烧炉', '污染物': 'NOX', '行索引': start_row + 3},
                    {'排放口': '焙烧炉', '污染物': 'SO2', '行索引': start_row + 4},
                ]
            
            # 处理每个季度的三个月数据
            months = [1, 2, 3] if quarter == 1 else [4, 5, 6] if quarter == 2 else [7, 8, 9] if quarter == 3 else [10, 11, 12]
            
            for month_idx, month in enumerate(months):
                # 智能查找月份数据列（每个月4列：浓度、排气量、时间、排放量）
                base_col = None
                
                # 查找月份标题
                for col in range(len(sheet_data.columns)):
                    if start_row > 0:
                        cell = sheet_data.iloc[start_row-1, col]
                        if cell and (f"{month}月" in str(cell) or f"{quarter}季度" in str(cell)):
                            base_col = col
                            break
                
                if base_col is None:
                    # 如果没找到月份标题，尝试根据位置计算
                    base_col = month_idx * 4 + 2  # 废气数据通常从第2列开始
                
                for data_row in data_rows:
                    row_idx = data_row['行索引']
                    
                    if row_idx >= len(sheet_data):
                        continue
                    
                    try:
                        # 浓度
                        conc_col = base_col
                        conc = sheet_data.iloc[row_idx, conc_col] if conc_col < len(sheet_data.columns) else 0
                        if pd.isna(conc):
                            conc = 0
                        
                        # 排气量
                        exhaust_col = base_col + 1
                        exhaust = sheet_data.iloc[row_idx, exhaust_col] if exhaust_col < len(sheet_data.columns) else 0
                        if pd.isna(exhaust):
                            exhaust = 0
                        
                        # 运行时间
                        time_col = base_col + 2
                        hours = sheet_data.iloc[row_idx, time_col] if time_col < len(sheet_data.columns) else 0
                        if pd.isna(hours):
                            hours = 0
                        
                        # 排放量（废气除以10^9）
                        emission_col_idx = base_col + 3
                        if emission_col_idx < len(sheet_data.columns):
                            emission = sheet_data.iloc[row_idx, emission_col_idx]
                            if pd.isna(emission):
                                emission = float(conc) * float(exhaust) * float(hours) / 1000000000
                        else:
                            emission = float(conc) * float(exhaust) * float(hours) / 1000000000
                        
                        # 添加到数据列表
                        self.exhaust_data.append({
                            '文件': os.path.basename(filepath),
                            '年份': year,
                            '季度': quarter,
                            '月份': f'{month}月',
                            '排放口': data_row['排放口'],
                            '污染物': data_row['污染物'],
                            '浓度(mg/m³)': float(conc),
                            '排气量(m³/h)': float(exhaust),
                            '运行时间(h)': float(hours),
                            '排放量(t)': float(emission) if not pd.isna(emission) else 0
                        })
                        
                    except Exception as e:
                        continue
            
            return True
            
        except Exception as e:
            print(f"⚠️  提取废气数据时出错（{os.path.basename(filepath)}）：{e}")
            return False
    
    def process_all_files(self):
        """处理所有Excel文件"""
        excel_files = self.find_excel_files()
        
        if not excel_files:
            print("❌ 没有找到Excel文件！")
            print("请确保Excel文件在程序同一目录下，且扩展名为.xlsx或.xls")
            return False
        
        success_count = 0
        
        for filepath in excel_files:
            try:
                print(f"\n📄 正在处理: {os.path.basename(filepath)}")
                
                # 从文件名提取年份和季度
                year, quarter = self.extract_year_quarter_from_filename(filepath)
                
                # 读取Excel文件，尝试所有sheet
                try:
                    xls = pd.ExcelFile(filepath)
                    sheet_names = xls.sheet_names
                    
                    # 智能识别废水sheet
                    water_sheet = None
                    for sheet in sheet_names:
                        sheet_lower = sheet.lower()
                        if '废水' in sheet_lower or 'water' in sheet_lower or '污水' in sheet_lower:
                            water_sheet = sheet
                            break
                    if water_sheet is None and len(sheet_names) > 0:
                        water_sheet = sheet_names[0]  # 默认第一个sheet
                    
                    # 智能识别废气sheet
                    exhaust_sheet = None
                    for sheet in sheet_names:
                        sheet_lower = sheet.lower()
                        if '废气' in sheet_lower or 'exhaust' in sheet_lower or 'air' in sheet_lower or 'gas' in sheet_lower:
                            exhaust_sheet = sheet
                            break
                    if exhaust_sheet is None and len(sheet_names) > 1:
                        exhaust_sheet = sheet_names[1]  # 默认第二个sheet
                    
                    # 读取sheet数据
                    if water_sheet:
                        water_df = pd.read_excel(filepath, sheet_name=water_sheet, header=None)
                        if self.extract_water_data(filepath, water_df, year, quarter):
                            print(f"  ✅ 废水数据提取成功")
                    
                    if exhaust_sheet and exhaust_sheet != water_sheet:
                        exhaust_df = pd.read_excel(filepath, sheet_name=exhaust_sheet, header=None)
                        if self.extract_exhaust_data(filepath, exhaust_df, year, quarter):
                            print(f"  ✅ 废气数据提取成功")
                    
                    success_count += 1
                    
                except Exception as e:
                    print(f"  ⚠️  读取文件时出错: {e}")
                    continue
                    
            except Exception as e:
                print(f"  ⚠️  处理文件时出错: {e}")
                continue
        
        print(f"\n📊 数据处理完成:")
        print(f"  - 成功处理文件: {success_count}/{len(excel_files)}")
        print(f"  - 废水数据记录: {len(self.water_data)} 条")
        print(f"  - 废气数据记录: {len(self.exhaust_data)} 条")
        
        return success_count > 0
    
    def get_dataframes(self):
        """返回整理好的DataFrame"""
        water_df = pd.DataFrame(self.water_data) if self.water_data else pd.DataFrame()
        exhaust_df = pd.DataFrame(self.exhaust_data) if self.exhaust_data else pd.DataFrame()
        
        return water_df, exhaust_df

# 2. 数据可视化类
class DataVisualizer:
    """数据可视化类"""
    
    def __init__(self, water_df, exhaust_df):
        self.water_df = water_df
        self.exhaust_df = exhaust_df
    
    def create_water_pollutant_trend_chart(self):
        """创建废水污染物年度趋势图"""
        if self.water_df.empty:
            return None
        
        try:
            # 按年份和月份汇总
            yearly_trend = self.water_df.groupby(['年份', '月份'])['排放量(t)'].sum().reset_index()
            
            # 创建时间线图表
            timeline = Timeline(init_opts=opts.InitOpts(width="1200px", height="600px"))
            
            years = sorted(yearly_trend['年份'].unique())
            
            for year in years:
                year_data = yearly_trend[yearly_trend['年份'] == year]
                
                # 确保月份顺序
                month_order = {f'{i}月': i for i in range(1, 13)}
                year_data['month_num'] = year_data['月份'].map(month_order)
                year_data = year_data.sort_values('month_num')
                
                line = (
                    Line()
                    .add_xaxis(year_data['月份'].tolist())
                    .add_yaxis(
                        "总排放量",
                        [round(x, 6) for x in year_data['排放量(t)'].tolist()],
                        is_smooth=True,
                        linestyle_opts=opts.LineStyleOpts(width=4),
                        label_opts=opts.LabelOpts(is_show=False),
                        itemstyle_opts=opts.ItemStyleOpts(color="#5470c6")
                    )
                    .set_global_opts(
                        title_opts=opts.TitleOpts(title=f"{year}年废水排放趋势"),
                        tooltip_opts=opts.TooltipOpts(trigger="axis"),
                        yaxis_opts=opts.AxisOpts(
                            name="排放量(t)",
                            axislabel_opts=opts.LabelOpts(formatter="{value} t")
                        )
                    )
                )
                timeline.add(line, f"{year}年")
            
            timeline.add_schema(
                play_interval=2000,
                is_timeline_show=True,
                is_auto_play=False,
                is_loop_play=False,
                pos_left="10%",
                pos_right="10%"
            )
            
            return timeline
            
        except Exception as e:
            print(f"创建废水趋势图时出错: {e}")
            return None
    
    def create_top_water_pollutants_chart(self):
        """创建废水主要污染物排行榜"""
        if self.water_df.empty:
            return None
        
        try:
            # 计算每种污染物的总排放量
            pollutant_totals = self.water_df.groupby('污染物')['排放量(t)'].sum().reset_index()
            pollutant_totals = pollutant_totals.sort_values('排放量(t)', ascending=True)
            
            # 只显示前10种
            top_pollutants = pollutant_totals.tail(10)
            
            bar = (
                Bar(init_opts=opts.InitOpts(width="1000px", height="500px"))
                .add_xaxis(top_pollutants['污染物'].tolist())
                .add_yaxis(
                    "总排放量(t)",
                    [round(x, 6) for x in top_pollutants['排放量(t)'].tolist()],
                    label_opts=opts.LabelOpts(
                        position="right",
                        formatter="{c} t"
                    ),
                    itemstyle_opts=opts.ItemStyleOpts(color="#91cc75")
                )
                .reversal_axis()
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="废水主要污染物排行榜"),
                    xaxis_opts=opts.AxisOpts(
                        name="排放量(t)",
                        axislabel_opts=opts.LabelOpts(formatter="{value} t")
                    ),
                    tooltip_opts=opts.TooltipOpts(
                        trigger="axis",
                        axis_pointer_type="shadow",
                        formatter="{b}: {c} t"
                    )
                )
            )
            
            return bar
            
        except Exception as e:
            print(f"创建污染物排行榜时出错: {e}")
            return None
    
    def create_exhaust_pollutant_distribution_chart(self):
        """创建废气污染物分布图"""
        if self.exhaust_df.empty:
            return None
        
        try:
            # 按污染物类型汇总
            pollutant_dist = self.exhaust_df.groupby('污染物')['排放量(t)'].sum().reset_index()
            
            pie = (
                Pie(init_opts=opts.InitOpts(width="800px", height="500px"))
                .add(
                    "",
                    [list(z) for z in zip(pollutant_dist['污染物'].tolist(), 
                                         [round(x, 6) for x in pollutant_dist['排放量(t)'].tolist()])],
                    radius=["30%", "75%"],
                    label_opts=opts.LabelOpts(
                        formatter="{b}: {c}t ({d}%)"
                    )
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="废气污染物排放分布"),
                    tooltip_opts=opts.TooltipOpts(
                        trigger="item",
                        formatter="{a}<br/>{b}: {c}t ({d}%)"
                    ),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_left="left")
                )
                .set_series_opts(
                    label_opts=opts.LabelOpts(position="outside")
                )
            )
            
            return pie
            
        except Exception as e:
            print(f"创建废气分布图时出错: {e}")
            return None
    
    def create_emission_source_comparison_chart(self):
        """创建排放源对比图"""
        if self.exhaust_df.empty:
            return None
        
        try:
            # 按排放口汇总
            source_dist = self.exhaust_df.groupby('排放口')['排放量(t)'].sum().reset_index()
            source_dist = source_dist.sort_values('排放量(t)', ascending=True).tail(10)  # 前10个
            
            bar = (
                Bar(init_opts=opts.InitOpts(width="1000px", height="500px"))
                .add_xaxis(source_dist['排放口'].tolist())
                .add_yaxis(
                    "排放量(t)",
                    [round(x, 6) for x in source_dist['排放量(t)'].tolist()],
                    itemstyle_opts=opts.ItemStyleOpts(color="#fac858"),
                    label_opts=opts.LabelOpts(
                        position="top",
                        formatter="{c} t"
                    )
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="主要废气排放源对比"),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(rotate=45)
                    ),
                    yaxis_opts=opts.AxisOpts(
                        name="排放量(t)",
                        axislabel_opts=opts.LabelOpts(formatter="{value} t")
                    ),
                    tooltip_opts=opts.TooltipOpts(trigger="axis")
                )
            )
            
            return bar
            
        except Exception as e:
            print(f"创建排放源对比图时出错: {e}")
            return None
    
    def create_quarterly_comparison_chart(self):
        """创建季度对比图"""
        if self.water_df.empty and self.exhaust_df.empty:
            return None
        
        try:
            # 汇总季度数据
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
            
            # 创建季度标签
            quarterly_df['季度标签'] = quarterly_df['年份'].astype(str) + '年Q' + quarterly_df['季度'].astype(str)
            quarterly_df = quarterly_df.sort_values(['年份', '季度'])
            
            # 创建图表
            line = (
                Line(init_opts=opts.InitOpts(width="1200px", height="500px"))
                .add_xaxis(quarterly_df['季度标签'].unique().tolist())
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="废水废气排放季度对比"),
                    tooltip_opts=opts.TooltipOpts(trigger="axis"),
                    yaxis_opts=opts.AxisOpts(
                        name="排放量(t)",
                        axislabel_opts=opts.LabelOpts(formatter="{value} t")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(rotate=45)
                    ),
                    legend_opts=opts.LegendOpts(pos_top="10%")
                )
            )
            
            # 添加废水数据系列
            water_data = quarterly_df[quarterly_df['类型'] == '废水']
            if not water_data.empty:
                water_values = []
                for quarter in quarterly_df['季度标签'].unique():
                    value = water_data[water_data['季度标签'] == quarter]['排放量(t)']
                    water_values.append(round(value.iloc[0], 6) if not value.empty else 0)
                
                line.add_yaxis(
                    "废水",
                    water_values,
                    is_smooth=True,
                    linestyle_opts=opts.LineStyleOpts(width=3),
                    itemstyle_opts=opts.ItemStyleOpts(color="#5470c6"),
                    label_opts=opts.LabelOpts(is_show=False)
                )
            
            # 添加废气数据系列
            exhaust_data = quarterly_df[quarterly_df['类型'] == '废气']
            if not exhaust_data.empty:
                exhaust_values = []
                for quarter in quarterly_df['季度标签'].unique():
                    value = exhaust_data[exhaust_data['季度标签'] == quarter]['排放量(t)']
                    exhaust_values.append(round(value.iloc[0], 6) if not value.empty else 0)
                
                line.add_yaxis(
                    "废气",
                    exhaust_values,
                    is_smooth=True,
                    linestyle_opts=opts.LineStyleOpts(width=3),
                    itemstyle_opts=opts.ItemStyleOpts(color="#ee6666"),
                    label_opts=opts.LabelOpts(is_show=False)
                )
            
            return line
            
        except Exception as e:
            print(f"创建季度对比图时出错: {e}")
            return None

# 3. 生成HTML报告
def generate_html_report(water_df, exhaust_df, visualizer):
    """生成完整的HTML报告"""
    
    # 创建标签页
    tab = Tab(page_title="废水废气排放综合分析报告")
    
    # 添加废水分析标签页
    if not water_df.empty:
        tab.add(visualizer.create_water_pollutant_trend_chart(), "废水排放趋势")
        tab.add(visualizer.create_top_water_pollutants_chart(), "废水污染物排行")
    
    # 添加废气分析标签页
    if not exhaust_df.empty:
        tab.add(visualizer.create_exhaust_pollutant_distribution_chart(), "废气污染物分布")
        tab.add(visualizer.create_emission_source_comparison_chart(), "废气排放源对比")
    
    # 添加综合分析标签页
    comparison_chart = visualizer.create_quarterly_comparison_chart()
    if comparison_chart:
        tab.add(comparison_chart, "季度对比分析")
    
    # 添加数据概览标签页
    overview_content = create_data_overview(water_df, exhaust_df)
    if overview_content:
        # 创建一个简单的图表来显示数据概览
        overview_chart = create_overview_chart(water_df, exhaust_df)
        if overview_chart:
            tab.add(overview_chart, "数据概览")
    
    # 生成HTML文件
    output_file = "废水废气排放综合分析报告.html"
    tab.render(output_file)
    
    # 美化HTML文件
    beautify_html(output_file, water_df, exhaust_df)
    
    return output_file

def create_overview_chart(water_df, exhaust_df):
    """创建数据概览图表"""
    try:
        # 计算基本统计数据
        stats = {
            '废水记录数': len(water_df) if not water_df.empty else 0,
            '废气记录数': len(exhaust_df) if not exhaust_df.empty else 0,
            '废水总排放': round(water_df['排放量(t)'].sum(), 6) if not water_df.empty else 0,
            '废气总排放': round(exhaust_df['排放量(t)'].sum(), 6) if not exhaust_df.empty else 0,
            '废水污染物数': water_df['污染物'].nunique() if not water_df.empty else 0,
            '废气污染物数': exhaust_df['污染物'].nunique() if not exhaust_df.empty else 0
        }
        
        # 创建一个简单的柱状图显示数据量
        bar = (
            Bar(init_opts=opts.InitOpts(width="800px", height="400px"))
            .add_xaxis(list(stats.keys())[:4])  # 只显示前4个统计项
            .add_yaxis(
                "数值",
                list(stats.values())[:4],
                label_opts=opts.LabelOpts(position="top"),
                itemstyle_opts=opts.ItemStyleOpts(color="#73c0de")
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="数据统计概览"),
                yaxis_opts=opts.AxisOpts(name="数值")
            )
        )
        
        return bar
        
    except Exception as e:
        print(f"创建概览图表时出错: {e}")
        return None

def create_data_overview(water_df, exhaust_df):
    """创建数据概览文本"""
    overview = "<h2>数据概览</h2>"
    
    if not water_df.empty:
        overview += f"""
        <h3>废水数据统计</h3>
        <ul>
            <li>数据记录数: {len(water_df)} 条</li>
            <li>污染物种类: {water_df['污染物'].nunique()} 种</li>
            <li>时间范围: {water_df['年份'].min()}年 - {water_df['年份'].max()}年</li>
            <li>总排放量: {water_df['排放量(t)'].sum():.6f} 吨</li>
        </ul>
        """
    
    if not exhaust_df.empty:
        overview += f"""
        <h3>废气数据统计</h3>
        <ul>
            <li>数据记录数: {len(exhaust_df)} 条</li>
            <li>污染物种类: {exhaust_df['污染物'].nunique()} 种</li>
            <li>排放源数量: {exhaust_df['排放口'].nunique()} 个</li>
            <li>总排放量: {exhaust_df['排放量(t)'].sum():.6f} 吨</li>
        </ul>
        """
    
    return overview

def beautify_html(filename, water_df, exhaust_df):
    """美化HTML文件，添加样式和数据表格"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 创建数据表格HTML
        data_tables = "<div style='margin: 40px;'>"
        
        if not water_df.empty:
            # 废水数据摘要表格
            water_summary = water_df.groupby(['年份', '季度', '污染物'])['排放量(t)'].sum().reset_index()
            water_summary = water_summary.pivot_table(
                index='污染物', 
                columns=['年份', '季度'], 
                values='排放量(t)',
                aggfunc='sum'
            ).round(6)
            
            data_tables += f"""
            <h2 style='color: #2c3e50;'>废水排放数据摘要（单位：吨）</h2>
            <div style='overflow-x: auto; margin-bottom: 40px;'>
                {water_summary.to_html(classes='data-table', border=1)}
            </div>
            """
        
        if not exhaust_df.empty:
            # 废气数据摘要表格
            exhaust_summary = exhaust_df.groupby(['年份', '季度', '污染物', '排放口'])['排放量(t)'].sum().reset_index()
            exhaust_summary = exhaust_summary.pivot_table(
                index=['污染物', '排放口'],
                columns=['年份', '季度'],
                values='排放量(t)',
                aggfunc='sum'
            ).round(6)
            
            data_tables += f"""
            <h2 style='color: #2c3e50;'>废气排放数据摘要（单位：吨）</h2>
            <div style='overflow-x: auto; margin-bottom: 40px;'>
                {exhaust_summary.to_html(classes='data-table', border=1)}
            </div>
            """
        
        data_tables += "</div>"
        
        # 添加CSS样式
        css_style = """
        <style>
            body {
                font-family: 'Microsoft YaHei', Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f7fa;
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
            
            .data-table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 12px;
            }
            
            .data-table th, .data-table td {
                border: 1px solid #ddd;
                padding: 8px 12px;
                text-align: center;
            }
            
            .data-table th {
                background-color: #007bff;
                color: white;
                font-weight: bold;
                position: sticky;
                top: 0;
            }
            
            .data-table tr:nth-child(even) {
                background-color: #f8f9fa;
            }
            
            .data-table tr:hover {
                background-color: #e9ecef;
            }
            
            .echarts-container {
                margin: 20px 0;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 1px 10px rgba(0,0,0,0.05);
            }
            
            .summary-box {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #28a745;
                margin: 20px 0;
            }
            
            .footer {
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #dee2e6;
                color: #6c757d;
                font-size: 12px;
            }
        </style>
        """
        
        # 在head标签中插入样式
        content = content.replace('</head>', css_style + '</head>')
        
        # 在body开始后添加标题
        title_section = """
        <div class="container">
            <div class="header">
                <h1>🏭 废水废气排放综合分析报告</h1>
                <p>基于2023-2025年季度监测数据 | 生成时间：""" + datetime.now().strftime('%Y年%m月%d日 %H:%M:%S') + """</p>
            </div>
        """
        content = content.replace('<body>', '<body>' + title_section)
        
        # 在图表后添加数据表格
        content = content.replace('</div></body>', data_tables + '</div></body>')
        
        # 添加页脚
        footer_section = """
            <div class="footer">
                <p>📊 报告说明：本报告基于智能数据提取技术，自动识别和解析废水废气排放数据</p>
                <p>⚠️ 数据仅供参考，具体以原始监测数据为准</p>
                <p>© 2023-2025 环境监测数据分析系统</p>
            </div>
        </div>
        """
        content = content.replace('</body>', footer_section + '</body>')
        
        # 重新写入文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ HTML报告美化完成")
        
    except Exception as e:
        print(f"⚠️  美化HTML文件时出错: {e}")

# 4. 主程序
def main():
    print("=" * 60)
    print("🏭 废水废气排放数据智能分析系统")
    print("=" * 60)
    print("🔍 正在搜索Excel文件...")
    
    # 初始化数据提取器
    extractor = SmartDataExtractor()
    
    # 处理所有文件
    if not extractor.process_all_files():
        print("\n❌ 数据处理失败，无法生成报告")
        return
    
    # 获取数据
    water_df, exhaust_df = extractor.get_dataframes()
    
    if water_df.empty and exhaust_df.empty:
        print("\n⚠️  没有提取到有效数据")
        return
    
    print(f"\n📊 数据提取完成:")
    if not water_df.empty:
        print(f"  - 废水数据: {len(water_df)} 条记录")
        print(f"    污染物种类: {water_df['污染物'].nunique()} 种")
        print(f"    时间范围: {water_df['年份'].min()}年 - {water_df['年份'].max()}年")
    
    if not exhaust_df.empty:
        print(f"  - 废气数据: {len(exhaust_df)} 条记录")
        print(f"    污染物种类: {exhaust_df['污染物'].nunique()} 种")
        print(f"    排放源数量: {exhaust_df['排放口'].nunique()} 个")
    
    # 创建可视化
    print("\n🎨 正在创建可视化图表...")
    visualizer = DataVisualizer(water_df, exhaust_df)
    
    # 生成报告
    print("📄 正在生成HTML报告...")
    output_file = generate_html_report(water_df, exhaust_df, visualizer)
    
    print(f"\n🎉 报告生成完成！")
    print(f"📁 报告文件: {output_file}")
    print(f"📏 文件大小: {os.path.getsize(output_file) / 1024:.1f} KB")
    print(f"\n💡 使用说明:")
    print(f"  1. 用浏览器打开 {output_file}")
    print(f"  2. 点击标签页切换不同图表")
    print(f"  3. 鼠标悬停查看详细数据")
    print(f"  4. 使用工具栏进行缩放、保存等操作")
    print(f"  5. 报告完全离线可用，无需联网")

if __name__ == "__main__":
    try:
        import glob
        main()
    except NameError:
        # 如果glob没有导入，先导入
        import glob
        main()