import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']     # 显示中文
# 为了坐标轴负号正常显示。matplotlib默认不支持中文，设置中文字体后，负号会显示异常。需要手动将坐标轴负号设为False才能正常显示负号。
matplotlib.rcParams['axes.unicode_minus'] = False
# 加载房地产数据和地铁站点数据的函数
def load_data():
    real_estate_data = pd.read_csv('data/WuHan.csv')
    subway_data = pd.read_csv('data/wh.csv')
    return real_estate_data, subway_data
# 匹配地铁站点和房地产价格数据
def match_data(subway_data, real_estate_data):
    matched_data = []
    for _, estate in real_estate_data.iterrows():
        lon, lat = estate['经度_百度坐标'], estate['纬度_百度坐标']
        if pd.isnull(lon) or pd.isnull(lat):
            continue
        nearest_station = find_nearest_station(subway_data, lon, lat)
        matched_data.append({
            'real_estate_price': float(estate['均价']),
            'station_name': nearest_station['站点名称'],
            'station_location': (nearest_station['gd经度'], nearest_station['gd纬度']),
            'station_distance': nearest_station['distance'],
            'estate_lon': lon,
            'estate_lat': lat
        })
    return pd.DataFrame(matched_data)

# 找到最近的地铁站
def find_nearest_station(subway_data, estate_lon, estate_lat):
    R = 6371
    def distance(row):
        return np.sqrt((row['gd经度'] - estate_lon)**2 + (row['gd纬度'] - estate_lat)**2)
    
    subway_data['distance'] = subway_data.apply(distance, axis=1)
    return subway_data.loc[subway_data['distance'].idxmin()]
# 保存匹配后的数据到CSV文件
real_estate_data, subway_data = load_data()
matched_data = match_data(subway_data, real_estate_data)
matched_data.to_csv('data/matched_data.csv', index=False)

# 加载所有匹配数据并进行相关性分析和可视化

matched_data = pd.read_csv('data/matched_data.csv')

# 相关性分析
corr, _ = pearsonr(matched_data['real_estate_price'], matched_data['station_distance'])
print(f'Pearson correlation coefficient: {corr}')

# 可视化
plt.figure(figsize=(12, 6))
sns.scatterplot(data=matched_data, x='station_distance', y='real_estate_price')
plt.title('到最邻近地铁站距离与价格散点图')
plt.xlabel('距离')
plt.ylabel('均价')
plt.show()
