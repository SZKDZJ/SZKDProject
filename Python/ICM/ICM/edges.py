import pandas as pd
import geopandas as gpd
import numpy as np
import ast
from shapely import wkt
from sklearn.preprocessing import LabelEncoder

data_edges_all = pd.read_csv("/Users/eureka/Desktop/2025_Problem_D_Data/edges_all.csv")
data_edges_drive = pd.read_csv("/Users/eureka/Desktop/2025_Problem_D_Data/edges_drive.csv")
data_Bus_Routes = pd.read_csv("/Users/eureka/Desktop/2025_Problem_D_Data/Bus_Routes.csv")

#bus_routes
data_Bus_Routes = data_Bus_Routes.drop(columns = 'Distributi')

#data_edges_all

#删去area列，由于缺乏数据
data_edges_all.drop('area', axis=1, inplace=True)

#===========================================填充缺失值============================================#
# 填充缺失值
columns_to_fill = ["tunnel", "bridge", "name", "junction", "ref", "access", "service"]
for col in columns_to_fill:
    if col in data_edges_all.columns:
        data_edges_all[col] = data_edges_all[col].fillna("unknown")
data_edges_all["lanes"] = data_edges_all["lanes"].fillna(-1)
data_edges_all["width"] = data_edges_all["width"].fillna(-1)

#===========================================数值替换==============================================#
# 替换 'junction' 列值并显式转换类型
if 'junction' in data_edges_all.columns:
    data_edges_all['junction'] = data_edges_all['junction'].replace({
        "circular": 1,
        "jughandle": 2,
        "roundabout": 3,
        "spui": 4,
        "frontage": 5
    })
data_edges_all['reversed'] = data_edges_all['reversed'].replace({"TRUE":1,"FALSE":0,"[False/True]":2})
data_edges_all["oneway"] = data_edges_all["oneway"].replace({"TRUE":1,"FALSE":0})

#=========================================处理maxspeed列===========================================#
# 定义清理函数
def clean_maxspeed(value):
    try:
        # 如果是字符串表示的列表，先转换为列表
        if isinstance(value, str) and value.startswith('[') and value.endswith(']'):
            # 去掉多余的空格和引号，将字符串转换为列表
            value = value.strip("[]").replace("'", "").replace('"', "").split(", ")

        # 如果是列表，去掉单位
        if isinstance(value, list):
            return [item.split(' ')[0] for item in value if 'mph' in item or item.isdigit()]

        # 如果是单个字符串，去掉单位并返回
        if isinstance(value, str):
            return value.split(' ')[0] if 'mph' in value else value

        # 其他情况直接返回原值或 NaN
        return value
    except Exception as e:
        print(f"Error processing value: {value}, error: {e}")
        return value

# 应用清理函数
data_edges_all['maxspeed'] = data_edges_all['maxspeed'].apply(clean_maxspeed)

# 转换成数值类型，跳过 NaN
data_edges_all["maxspeed"] = pd.to_numeric(data_edges_all["maxspeed"], errors='coerce')

# 手动填充的数据：key为highway类型，value为对应的maxspeed
manual_fills = {
    'path': 3,
    'footway':3,
    'steps':3,
    'track':25,
    'bridleway':6,
    'bus_stop':5,
    'busway':30,
    'corridor':10,
    'disused':3,
    'living_street':25,
    'secondary_link':30,
    'cycleway':10,
    'tertiary_link':30,
    'services':5,
    'steps':3,
    'pedestrian':5,
    'motorway':65,
    'motorway_link':65,
    'residential':25,
    'primary':55,
    'track':25,
    'tertiary':35,
    'service':25,
    'secondary':55,
    'unclassified':25,
    'primary_link':55,
    'trunk':55,
    'trunk_link':55,
    'pedestrian':5,
    'bridleway':10,
}
def fill_missing_maxspeed(df):

    highway_maxspeed_dist = {}
    t_set = set()

    for highway_value, group in df.groupby('highway'):
        non_missing_values = group['maxspeed'].dropna()

        if len(non_missing_values) > 100:
            value_counts = non_missing_values.value_counts(normalize=True)
            highway_maxspeed_dist[tuple(highway_value)] = value_counts

    for idx, row in df.iterrows():
        if pd.isna(row['maxspeed']):
            highway_type = row['highway']
            if isinstance(row['highway'], str) and row['highway'].startswith('[') and row['highway'].endswith(']'):
                try:
                    row['highway'] = ast.literal_eval(row['highway'])
                except Exception as e:
                    print(f"Error converting row {idx}: {e}")

            if not isinstance(row['highway'], list):
                row['highway'] = [row['highway']]

            fill_values = []
            for highway_type in row['highway']:
                if tuple(highway_type) in highway_maxspeed_dist:
                    value_counts = highway_maxspeed_dist[tuple(highway_type)]
                    chosen_value = int(np.random.choice(value_counts.index, p=value_counts.values))
                    fill_values.append(chosen_value)
                else:
                    fill_values.append(manual_fills[highway_type])  # 如果没有数据，

            if len(fill_values) == 1:
                fill_values = fill_values[0]
            if len(row['highway']) == 1:
                row['highway'] = row['highway'][0]
            print(row['highway'], fill_values)
            df.at[idx, 'maxspeed'] = str(fill_values)
    return df

data_edges_all = fill_missing_maxspeed(data_edges_all)

#data_edges_drive

#===========================================填充缺失值============================================#
# 填充缺失值
columns_to_fill = ["tunnel", "bridge", "name", "junction", "ref", "access", "service"]
for col in columns_to_fill:
    if col in data_edges_drive.columns:
        data_edges_drive[col] = data_edges_drive[col].fillna("unknown")

data_edges_drive["lanes"] = data_edges_drive["lanes"].fillna(-1)
data_edges_drive["width"] = data_edges_drive["width"].fillna(-1)

#===========================================数值替换==============================================#
# 替换 'junction' 列值并显式转换类型
if 'junction' in data_edges_drive.columns:
    data_edges_drive['junction'] = data_edges_drive['junction'].replace({
        "circular": 1,
        "jughandle": 2,
        "roundabout": 3,
        "spui": 4,
        "frontage": 5
    })
data_edges_drive['reversed'] = data_edges_drive['reversed'].replace({"TRUE":1,"FALSE":0,"[False/True]":2})
data_edges_drive["oneway"] = data_edges_drive["oneway"].replace({"TRUE":1,"FALSE":0})
data_edges_drive['maxspeed'] = data_edges_drive['maxspeed'].apply(clean_maxspeed)

# 转换成数值类型，跳过 NaN
data_edges_drive["maxspeed"] = pd.to_numeric(data_edges_all["maxspeed"], errors='coerce')
data_edges_drive = fill_missing_maxspeed(data_edges_drive)
#===========================================保存数据==============================================#
#data_Bus_Routes.to_excel("Bus_RoutesNew.xlsx")
data_edges_all.to_excel("edges_allNew.xlsx")
data_edges_drive.to_excel("edges_driveNew.xlsx")