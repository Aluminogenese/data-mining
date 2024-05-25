import pandas as pd
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
token='pk.eyJ1IjoicHl0aG9uYmlyZCIsImEiOiJja2tqOTBneXcwZTlyMnRzNzczNngzY2huIn0.2dImfhmc06Z8IeX6WeNamQ'

data=pd.read_csv('data/WuHan.csv')

fig = px.scatter_mapbox(data,
                        lon = '经度_WGS1984坐标',  #输入经度坐标
                        lat = '纬度_WGS1984坐标',  #输入纬度
                        color ="均价", #对应excel的color栏，每个值代表一种颜色
                        hover_name ="小区名称",#可以对应excel里面的某一栏
                        # size_max = 16, #上面size尺寸的最大值
                        color_continuous_scale = px.colors.carto.Temps
                       )
 
fig.update_layout(mapbox = {'accesstoken': token, #需要到官网注册一个token
                            "center":{'lon':114.381664213935,'lat':30.8778349434214},  #指定的地图中心
                            'zoom': 7.48,
                            'style': 'dark', #显示的地图类型，有遥感地图，街道地图等类型
                           },
                  margin = {'l': 0, 'r': 0, 't': 0, 'b': 0})


url='https://map.amap.com/service/subway?_1684218731379&srhdata=4201_drw_wuhan.json'
response=requests.get(url)
result=json.loads(response.text)
stations=[]
lats=[]
lons=[]
lines=[]
for i in result['l']:
    for j in i['st']:
        lines.append(i['kn'])
        stations.append(j['n'])
        lons.append(j['sl'].split(',')[0])
        lats.append(j['sl'].split(',')[1])
dataframe=pd.DataFrame({'站名':stations,'线路':lines,'经度':lons,'纬度':lats})

lines=dataframe['线路'].unique().tolist()
for line in lines:
    fig.add_traces(go.Scattermapbox(
        mode="markers+lines",
        lon=dataframe.loc[lambda x:x['线路']==line]['经度'],
        lat=dataframe.loc[lambda x:x['线路']==line]['纬度'],
        hovertext=dataframe.loc[lambda x:x['线路']==line]['站名'],
        hoverinfo='text',
        marker_symbol='marker',
        marker_size=6,
        showlegend = False))
for line in lines[1:]:
    fig.add_traces(go.Scattermapbox(
        mode="markers+lines",
        lon=dataframe.loc[lambda x:x['线路']==line]['经度'],
        lat=dataframe.loc[lambda x:x['线路']==line]['纬度'],
        hovertext=dataframe.loc[lambda x:x['线路']==line]['站名'],
        hoverinfo='text',
        marker_symbol='marker',
        marker_size=6,
        showlegend = False))
fig.update_layout(mapbox={"accesstoken":token,"center":{'lon':114.381664213935,'lat':30.8778349434214},'zoom':11.8},
                  margin={'l':0,'r':0,'t':0,"b":0})

fig.show() #显示地图
