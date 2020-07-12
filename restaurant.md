# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

from bokeh.plotting import figure,show,output_file
from bokeh.models import ColumnDataSource


'''
（1）加载数据
'''
df1 = pd.read_excel('上海餐饮数据.xlsx', sheet_name = 0)

'''
（2）计算指标：口味、客单价、性价比指标
'''
## 数据清洗 + 性价比计算
data1 = df1[['类别','点评数','口味','环境','服务','人均消费']]
data1.dropna(inplace = True)
data1 = data1[(data1['口味']>0) & (data1['人均消费'] > 0)]
data1['性价比']  = (data1['口味'] + data1['服务'] + data1['环境'])/data1['人均消费']

## 创建函数1: 制作箱型图，查看异常值
def f1():
    fig,axes = plt.subplots(1,3,figsize=(10,4))
    data1.boxplot(column = ['口味'],ax = axes[0])
    data1.boxplot(column = ['人均消费'],ax = axes[1])
    data1.boxplot(column = ['性价比'],ax = axes[2])

## 创建函数2： 清除异常值
def f2(data,col):
    q1 = data1[col].quantile(q=0.25)
    q3 = data1[col].quantile(q=0.75)
    iqr = q3-q1
    t2 = q3 + 1.5 * iqr
    t1 = q1 - 1.5 * iqr
    return data1[(data1[col] > t1) & (data1[col] < t2)][['类别',col]]

data_xjb = f2(data1,'性价比')
data_rj = f2(data1,'人均消费')
data_rj = f2(data_rj,'人均消费')
data_kw = f2(data1,'口味')

## 创建函数3： 标准化指标并进行排序
def f3(data,col):
    col_name = col+'_norm'
    data_gp = data.groupby('类别').mean()
    data_gp[col_name] = (data_gp[col]-data_gp[col].min())/(data_gp[col].max()-data_gp[col].min())
    data_gp.sort_values(by = col_name, inplace = True, ascending = False)
    return data_gp

data_kw_score = f3(data_kw,'口味')
data_rj_score = f3(data_rj,'人均消费')
data_xjb_score = f3(data_xjb,'性价比')
    
data_final_q1 = pd.merge(data_kw_score,data_rj_score, left_index=True, right_index=True) 
data_final_q1 = pd.merge(data_final, data_xjb_score, left_index=True, right_index=True) 

'''
(3) 绘制图表 辅助分析
'''
from bokeh.models import HoverTool
from bokeh.palettes import brewer
from bokeh.models.annotations import BoxAnnotation
from bokeh.layouts import gridplot

## 将列名改为英文
data_final['size'] = data_final_q1['kw_norm'] * 40  # 添加size字段
data_final.index.name = 'type'
data_final.columns = ['kw','kw_norm','price','price_norm','xjb','xjb_norm','size']

                         
## 创建数据
source = ColumnDataSource(data_final)
hover = HoverTool(tooltips=[("餐饮类型", "@type"),
                            ("人均消费", "@price"),
                            ("性价比得分", "@xjb_norm"),
                            ("口味得分", "@kw_norm")
                           ])  # 设置标签显示内容
    
result = figure(plot_width=800, plot_height=250,
                title="餐饮类型得分情况" ,
                x_axis_label = '人均消费', y_axis_label = '性价比得分', 
                tools=[hover,'box_select,reset,xwheel_zoom,pan,crosshair']) 

# 散点图
result.circle(x = 'price',y = 'xjb_norm',source = source,
         line_color = 'black',line_dash = [6,4],fill_alpha = 0.6,
        size = 'size')

# 设置人均消费中间价位区间
price_mid = BoxAnnotation(left=40,right=80, fill_alpha=0.1, fill_color='navy')   
result.add_layout(price_mid)

result.title.text_font_style = "bold"
result.ygrid.grid_line_dash = [6, 4]
result.xgrid.grid_line_dash = [6, 4]


# 绘制柱状图
data_type = data_final_q1.index.tolist()# 提取横坐标

kw = figure(plot_width=800, plot_height=250, title='口味得分',x_range=data_type,
           tools=[hover,'box_select,reset,xwheel_zoom,pan,crosshair'])
kw.vbar(x='type', top='kw_norm', source=source,width=0.9, alpha = 0.8,color = 'red')   
kw.ygrid.grid_line_dash = [6, 4]
kw.xgrid.grid_line_dash = [6, 4]
# 柱状图1

price = figure(plot_width=800, plot_height=250, title='人均消费得分',x_range=kw.x_range,
              tools=[hover,'box_select,reset,xwheel_zoom,pan,crosshair'])
price.vbar(x='type', top='price_norm', source=source,width=0.9, alpha = 0.8,color = 'green') 
price.ygrid.grid_line_dash = [6, 4]
price.xgrid.grid_line_dash = [6, 4]
# 柱状图2
    
p = gridplot([[result],[kw], [price]])


show(p)











    
    
    
    
    
    
    
    
    
    
    
    
    
    

print('Finish')
