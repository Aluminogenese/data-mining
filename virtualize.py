import pyecharts
import pandas as pd
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.datasets import register_url
from pyecharts.globals import ThemeType
from pyecharts.globals import GeoType
import seaborn as sns  
import matplotlib.pyplot as plt
import math
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']     # 显示中文
# 为了坐标轴负号正常显示。matplotlib默认不支持中文，设置中文字体后，负号会显示异常。需要手动将坐标轴负号设为False才能正常显示负号。
matplotlib.rcParams['axes.unicode_minus'] = False

data = pd.read_csv("data/WuHan.csv", encoding="utf8")
dataList = data.to_dict(orient='records')
try:
    register_url("https://echarts-maps.github.io/echarts-china-counties-js/")
except Exception:
    import ssl
 
    ssl._create_default_https_context = ssl._create_unverified_context
    register_url("https://echarts-maps.github.io/echarts-china-counties-js/")
geo=Geo(init_opts=opts.InitOpts(theme=ThemeType.DARK,
                                width="100%",
                                height="700px",
                                page_title="武汉市2018年房价数据可视化",
                                bg_color="black"))
 
geo.add_schema(maptype='武汉',
               label_opts=opts.LabelOpts(is_show=True),
               itemstyle_opts=opts.ItemStyleOpts(color="black", border_color="#1E90FF", border_width=1.5))
 
data_pair = []
for item in dataList:
    name = item["小区名称"]
    value = item["均价"]
 
    longitude = item["经度_百度坐标"]
    latitude = item["纬度_百度坐标"]
    # 将楼房坐标添加到地图中
    geo.add_coordinate(name, longitude, latitude)
    data_pair.append((name, value))
# 添加数据项，即为地图中楼房位置赋值
geo.add("房价",
        data_pair=data_pair,
        type_="scatter",
        symbol_size=1.5,
        is_large=True,
        )
# 配置分组颜色
pricePieces = [
    {"max": 10000, "label":"1W以下", "color": "#F0F0BF"},
    {"min": 10000, "max": 20000, "label": "1W~2W", "color": "#08830A"},
    {"min": 20000, "max": 30000, "label": "2W~3W", "color": "#EA760F"},
    {"min": 30000, "max": 40000, "label": "3W~4W", "color": "#E800FF"},
    {"min": 40000, "label": "4W以上", "color": "#FF0005"},
]
geo.js_dependencies.add("echarts-gl")
geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
geo.set_global_opts(title_opts=opts.TitleOpts(title="武汉市房价数据可视化", pos_left="left", title_textstyle_opts=opts.TextStyleOpts(color="red")),
                    visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pricePieces))
geo.render("武汉Geo.html")

print(data["均价"].max())
# 查看总体房价直方图----------------------------
sns.displot(data["均价"],
            kde_kws={"color": "r", "lw": 1, "label": "KDE"},
            color="purple"
            )
plt.title("全市房价总体分布直方图")
plt.show()

my_order = data.groupby(by=["区域"])["均价"].median().sort_values(ascending=False).index
print(data.groupby(by=["区域"])["均价"].median().sort_values(ascending=False))
print(my_order)
# sns.catplot(x='区域', y='均价', data=data, order=my_order, kind="violin") # 绘制小提琴图
sns.boxplot(x='区域', y='均价', data=data, order=my_order)
plt.title("各区房价箱型图")
plt.show()

x = data.groupby(by=["区域"])["均价"].median().sort_values(ascending=False).index
y = data.groupby(by=["区域"])["均价"].median().sort_values(ascending=False).values
ax = sns.barplot(x=x,y=y)
print(data.groupby(by=["区域"])["均价"].median().sort_values(ascending=False).reset_index())
for index,row in data.groupby(by=["区域"])["均价"].median().sort_values(ascending=False).reset_index().iterrows():
    ax.text(row.name, row["均价"], row["均价"],color="red", ha="center")
plt.title("各区房价中位数柱形图")
plt.show()

centerPoint = (114.311754, 30.598604)
R = 6371
data["distance"] = data[["经度_百度坐标", "纬度_百度坐标"]].apply(lambda x: math.fabs(R*math.acos(math.cos(x["纬度_百度坐标"]*math.pi/180)*math.cos(centerPoint[1]*math.pi/180)*math.cos(x["经度_百度坐标"]*math.pi/180-centerPoint[0]*math.pi/180)+math.sin(x["纬度_百度坐标"]*math.pi/180)*math.sin(centerPoint[1]*math.pi/180))),
                                                      axis=1)
print(data[["经度_百度坐标", "纬度_百度坐标", "distance"]])
data["buildingType"].loc[data["buildingType"] == 0] = "未知类型"
data["buildingType"].loc[data["buildingType"] == 1] = "板楼"
data["buildingType"].loc[data["buildingType"] == 2] = "塔楼"
data["buildingType"].loc[data["buildingType"] == 3] = "板塔结合"
sns.scatterplot(data=data,
                x='distance',
                y='均价',
                hue="buildingType",   # 设置分组颜色
                style='区域',         # 设置分组样式
                size='propertyExpense'          # 设置分组大小
                )
plt.title("楼房离市中心的距离与价格散点图")
plt.show()