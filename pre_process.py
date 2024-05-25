import pandas as pd
# 读取数据
data = pd.read_excel("data/武汉市房价数据.xlsx")
#查看数据基本信息
print(data)
print(data.info())

# 地铁字段处理，提取地铁线路数字：
metro = []
for i in range(len(data["地铁"])):
    metroStation = data["地铁"][i]
    if pd.isnull(metroStation):   # 当不存在地铁时
        metro.append(0)           # 0 表示附近无地铁站
    else:                        # 当存在地铁时，提取地铁编号
        lineNum = metroStation[metroStation.index("铁") + 1: metroStation.index("号")]
        metro.append(int(lineNum))
data["metro"] = metro
data.drop('地铁',axis=1,inplace=True) # 删除原有的“地铁字段”
print(data[0:10])
print(data.info())

year = []
for i in range(len(data["建筑年代"])):
    yearNum =  data["建筑年代"][i]
    if yearNum == "暂无信息":
        year.append(0) # 0 代表未知
    else:
        year.append(int(yearNum[0:-1]))
data["year"] = year
data.drop('建筑年代',axis=1,inplace=True)
print(data[["小区名称","year"]][0:10])
print(data.info())

buildingType = []
for i in range(len(data["建筑类型"])):
    type = data["建筑类型"][i]
    if type == "未知类型":
        buildingType.append(0)
        # print(0)
    elif type == "板楼":
        buildingType.append(1)
        # print(1)
    elif type == "塔楼":
        buildingType.append(2)
        # print(2)
    else:
        buildingType.append(3)
        # print(3)
data["buildingType"] = buildingType
data.drop('建筑类型',axis=1,inplace=True)
print(data[["小区名称","buildingType"]][0:10])
print(data.info())

propertyExpense = []
for i in range(len(data["物业费用"])):
    expense = data["物业费用"][i]
    if expense == "暂无信息":
        propertyExpense.append(-1)
        # print(-1)
    elif "至" in expense:
        minPrice = float(expense[0 : expense.index("至")])
        maxPrice = float(expense[expense.index("至")+1 : expense.index("元")])
        price = round((minPrice+maxPrice)/2, 2)
        propertyExpense.append(price)
        # print(price)
    else:
        price = float(expense[0 : expense.index("元")])
        propertyExpense.append(price)
        # print(price)
data["propertyExpense"] = propertyExpense
data.drop('物业费用',axis=1,inplace=True)
print(data[["小区名称","propertyExpense"]][0:10])
print(data.info())

# 楼栋总数字段处理，去掉”栋“字，将字段值的类型改为数值型
data["楼栋总数"] = data["楼栋总数"].apply(lambda x: int(x[0:-1]))
# 房屋总数字段处理，去掉”户“字，将字段值的类型改为数值型
data["房屋总数"] = data["房屋总数"].apply(lambda x: int(x[0:-1]))
print(data.info())
print(data[["小区名称","楼栋总数", "房屋总数"]])

data.to_csv("WuHan.csv", encoding="utf8",index=False)
newData = pd.read_csv("WuHan.csv")
print(newData.info())