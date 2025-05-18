import pandas as pd
import numpy as np
import networkx as nx
import re
#导入公交站点数据
bus_stop = pd.read_csv("/Users/eureka/Desktop/2025_Problem_D_Data/Bus_Stops.csv")
#=======================================处理stop_name列=========================================#
def keep_lowercase(text):
    # 提取末尾部分的小写字母和空格
    match = re.search(r'[a-z ]+$', text)
    return match.group(0) if match else ''
bus_stop["stop_name"] = bus_stop["stop_name"].apply(keep_lowercase)
#==========================================stop_id列===========================================#
bus_stop = bus_stop.set_index("stop_id")
#===========================================数值替换============================================#
bus_stop['County'] = bus_stop['County'].replace({"Baltimore City":1,"Baltimore County":2})
bus_stop['Shelter'] = bus_stop['Shelter'].replace({"Yes":1 ,"No":0})
bus_stop['Mode'] = bus_stop['Mode'].replace({"Bus":1 ,"Bus/Commuter Bus":2,"Commuter Bus":3})
#=======================================删除Distributi列========================================#
bus_stop = bus_stop.drop(columns = 'Distributi')
bus_stop.to_excel("bus_stopNew.xlsx")

#nodes_all
nodes_all = pd.read_csv("/Users/eureka/Desktop/2025_Problem_D_Data/nodes_all.csv")

#========================================处理railway列==========================================#
nodes_all['railway'] = nodes_all['railway'].fillna(0)
nodes_all['railway'] = nodes_all['railway'].replace({"level_crossing":1 ,"subway_entrance":2})

#========================================处理highway列==========================================#
nodes_all['highway'] = nodes_all['highway'].fillna(0)
# 将列中的值替换为数字
nodes_all["highway"] = nodes_all["highway"].replace({'crossing':1, 'motorway_junction':2, 'mini_roundabout':3, 'elevator':4, 'traffic_signals':5, 'speed_camera':6, 'turning_loop':7, 'stop':8, 'turning_circle':9, 'give_way':10})
#=========================================处理ref列=============================================#
nodes_all['ref'] = nodes_all['ref'].fillna(0)

#========================================处理junction列=========================================#
nodes_all['junction'] = nodes_all['junction'].fillna(0)
nodes_all['junction'] = nodes_all['junction'].replace({"mini_roundabout":1, "roundabout":2,"yes":3})
#=====================================按照street_count分组======================================#

nodes_all = nodes_all.groupby('street_count')
dfs2 = {category: group.reset_index(drop=True) for category, group in nodes_all}
# 输出分组后的 DataFrame
for category, group_df in dfs2.items():
    print(f"Category: {category}")
    print(group_df)
    print("-" * 20)
with pd.ExcelWriter("node_allNew.xlsx") as writer:
    for category, group_df in dfs2.items():
        group_df.to_excel(writer, sheet_name=f"street_count_{category}", index=False)
print("所有分组数据已保存到node_allNew.xlsx")

#nodes_drive
nodes_drive = pd.read_csv("/Users/eureka/Desktop/2025_Problem_D_Data/nodes_drive.csv")
#========================================处理railway列==========================================#
nodes_drive['railway'] = nodes_drive['railway'].fillna(0)
nodes_drive['railway'] = nodes_drive['railway'].replace({"level_crossing":1 ,"subway_entrance":2})
#========================================处理highway列==========================================#
nodes_drive['highway'] = nodes_drive['highway'].fillna(0)
# 将列中的值替换为数字
nodes_drive["highway"] = nodes_drive["highway"].replace({'crossing':1, 'motorway_junction':2, 'mini_roundabout':3, 'elevator':4, 'traffic_signals':5, 'speed_camera':6, 'turning_loop':7, 'stop':8, 'turning_circle':9, 'give_way':10})
#=========================================处理ref列=============================================#
nodes_drive['ref'] = nodes_drive['ref'].fillna(0)

#========================================处理junction列=========================================#
nodes_drive['junction'] = nodes_drive['junction'].fillna(0)
nodes_drive['junction'] = nodes_drive['junction'].replace({"mini_roundabout":1, "roundabout":2,"yes":3})
#=====================================按照street_count分组======================================#

nodes_drive = nodes_drive.groupby('street_count')
dfs3 = {category: group.reset_index(drop=True) for category, group in nodes_drive}
# 输出分组后的 DataFrame
for category, group_df in dfs3.items():
    print(f"Category: {category}")
    print(group_df)
    print("-" * 20)

with pd.ExcelWriter("node_driveNew.xlsx") as writer:
    for category, group_df in dfs3.items():
        group_df.to_excel(writer, sheet_name=f"street_count_{category}", index=False)
print("所有分组数据已保存到node_driveNew.xlsx")
