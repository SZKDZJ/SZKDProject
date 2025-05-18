import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from shapely import wkt
import geopandas as gpd
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle
from shapely.geometry import Point
import heapq
import ast
from geopy.distance import geodesic
from sklearn.cluster import DBSCAN, KMeans
from scipy.spatial.distance import cdist
from sklearn.preprocessing import StandardScaler
import itertools
from collections import defaultdict
from tqdm import tqdm
import time

# 常量：需要移除的大桥标识
BRIDGE_REF = "I 695"

# 假设BPR函数中的经验参数
alpha = 0.15
beta = 4


# ============================ 读取数据 ============================ #
def load_aadt(path):
    print("Loading AADT data...")
    """加载流量数据"""
    try:
        df = pd.read_csv(path, encoding='utf-8-sig')
        df.columns = df.columns.str.strip().str.lower().str.replace(r'[^\w]', '_', regex=True).str.replace(r'_+', '_',
                                                                                                           regex=True)

        column_mapping = {
            'node start': 'node_start',  # 映射 'node start' 为 'node_start'
            'node(s) end': 'node_s_end',  # 映射 'node(s) end' 为 'node_s_end'
            'aadt': 'aadt_current_',  # AADT 列名
            'lanes': 'number_of_lanes'  # 车道数列名
        }

        df_clean = df.rename(columns=column_mapping)

        def safe_int_conversion(value):
            """尝试转换为整数，如果失败则返回默认值0"""
            try:
                return int(''.join(filter(str.isdigit, str(value))))
            except ValueError:
                return 0

        df_clean['u'] = df_clean['node_start'].apply(safe_int_conversion)
        df_clean['v'] = df_clean['node_s_end'].apply(safe_int_conversion)

        df_clean = df_clean.query('u > 0 and v > 0')  # 过滤有效的节点数据
        return df_clean[['u', 'v', 'aadt_current_', 'number_of_lanes']].reset_index(drop=True)
    except Exception as e:
        print(f"错误: {e}")
        raise


# 使用时
aadt_data = load_aadt("/Users/eureka/Desktop/2025_Problem_D_Data/MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.csv")


# 读取所有节点和边的数据
def read_edges_and_nodes(files):
    """读取多个 Excel 文件并返回合并后的 DataFrame"""
    return pd.concat([pd.read_excel(file) for file in files], ignore_index=True)


edges_all = read_edges_and_nodes(["edges_allNew.xlsx"])
edges_drive = read_edges_and_nodes(["edges_driveNew.xlsx"])
nodes_all = read_edges_and_nodes(["/Users/eureka/PycharmProjects/ICM/node_allNew.xlsx"])
nodes_drive = read_edges_and_nodes(["/Users/eureka/PycharmProjects/ICM/node_driveNew.xlsx"])


# 解析几何数据
def parse_geometry(dataframe, column='geometry'):
    """解析几何数据并转换为 Shapely 对象"""
    dataframe[column] = dataframe[column].apply(wkt.loads)
    return gpd.GeoDataFrame(dataframe, geometry=column)


gdf_edges_all = parse_geometry(edges_all)
gdf_edges_drive = parse_geometry(edges_drive)
gdf_nodes_all = parse_geometry(nodes_all)
gdf_nodes_drive = parse_geometry(nodes_drive)


# 确保坐标系统一致
def set_crs_to_4326(gdf):
    """设置 GeoDataFrame 的 CRS 为 EPSG:4326"""
    gdf.set_crs("EPSG:4326", allow_override=True, inplace=True)


set_crs_to_4326(gdf_edges_all)
set_crs_to_4326(gdf_edges_drive)
set_crs_to_4326(gdf_nodes_all)
set_crs_to_4326(gdf_nodes_drive)

# 执行空间连接
nodes_with_edges_all = gpd.sjoin(gdf_nodes_all, gdf_edges_all, how="left", predicate='intersects')
nodes_with_edges_drive = gpd.sjoin(gdf_nodes_drive, gdf_edges_drive, how="left", predicate='intersects')


# ============================ 网络构建 ============================ #
class EnhancedTrafficNetwork:
    def __init__(self):
        self.G = nx.DiGraph()
        self.edge_mapping = {}

    def build_network(self, nodes_gdf, edges_gdf, aadt_df):
        print("Building network...")
        """构建带流量属性的交通网络"""
        # 添加节点
        for _, row in nodes_gdf.iterrows():
            self.G.add_node(row['osmid'], pos=(row['geometry'].x, row['geometry'].y),
                            **row.drop(['geometry', 'osmid']).to_dict())

        # 添加边并合并流量数据
        edges_merged = edges_gdf.merge(aadt_df, on=['u', 'v'], how='left', suffixes=('', '_aadt'))
        for _, row in edges_merged.iterrows():
            self.add_edge(row)

    def add_edge(self, row):
        """向图中添加边及其属性"""
        attrs = {
            'length': row['length'],
            'maxspeed': self._parse_speed(row['maxspeed']),
            'lanes': row.get('lanes', 1),
            'bridge': row.get('bridge', 'no'),
            'ref': row.get('ref', '')
        }
        traffic_attrs = {
            'AADT': row.get('AADT', 0),
            'AADT_car': row.get('AADT Car', 0),
            'AADT_truck': row.get('AADT Light Truck', 0),
            'AADT_bus': row.get('AADT Bus', 0)
        }
        self.G.add_edge(row['u'], row['v'], **{**attrs, **traffic_attrs})
        self.edge_mapping[(row['u'], row['v'])] = traffic_attrs

    def _parse_speed(self, speed_str):
        """解析速度字符串"""
        try:
            if isinstance(speed_str, str):
                if '[' in speed_str:
                    return max(eval(speed_str))
                elif 'mph' in speed_str:
                    return float(speed_str.replace(' mph', '')) * 1.60934  # 转为km/h
            return float(speed_str)
        except:
            return 60  # 默认值

    def remove_bridge_edges(self):
        """移除大桥相关边"""
        edges_to_remove = [(u, v) for u, v, attrs in self.G.edges(data=True) if
                           attrs.get('ref') == BRIDGE_REF and attrs.get('bridge') == 'yes']
        self.G.remove_edges_from(edges_to_remove)
        return edges_to_remove


# 创建交通网络并构建
network = EnhancedTrafficNetwork()
network.build_network(gdf_nodes_all, gdf_edges_all, aadt_data)
edges_to_remove = network.remove_bridge_edges()

# 获取大桥相关的节点
start_nodes_b = [u for u, v in edges_to_remove]
end_nodes_b = [v for u, v in edges_to_remove]
bridge_nodes = set(start_nodes_b + end_nodes_b)
print(len(bridge_nodes))
print(bridge_nodes)

# ============================ A* 最短路径计算 ============================ #

# 为了优化性能，使用缓存存储计算过的启发式估算值和路径。
heuristic_cache = {}
path_cache = {}


def a_star_shortest_path(graph, start, end):
    print("Calculating shortest path...")
    """A*算法计算最短路径"""
    if (start, end) in path_cache:
        return path_cache[(start, end)]

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start] = heuristic_cost_estimate(graph, start, end)

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == end:
            path = reconstruct_path(came_from, current)
            path_cache[(start, end)] = (path, g_score[current])
            return path, g_score[current]

        for neighbor in graph.neighbors(current):
            edge_data = graph[current][neighbor]
            edge_length = edge_data.get('length', 1)
            edge_speed = edge_data.get('maxspeed')
            edge_speed = float(edge_speed) if isinstance(edge_speed, str) else float(
                max(eval(edge_speed)) if isinstance(edge_speed, list) else edge_speed)
            time = edge_length / edge_speed if edge_speed else 1
            tentative_g_score = g_score[current] + time

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic_cost_estimate(graph, neighbor, end)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return [], float('inf')  # No path found


def heuristic_cost_estimate(graph, start, goal):
    """启发式估算函数：计算两节点间的直线距离"""
    if (start, goal) in heuristic_cache:
        return heuristic_cache[(start, goal)]

    start_pos = graph.nodes[start].get('pos')
    goal_pos = graph.nodes[goal].get('pos')
    if start_pos and goal_pos:
        distance = geodesic(start_pos, goal_pos).kilometers
        heuristic_cache[(start, goal)] = distance
        return distance
    return float('inf')


def reconstruct_path(came_from, current):
    """重建路径"""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]


# ============================ 计算大桥节点之间的两两最短路径 ============================ #

results = {}
bridge_nodes = list(bridge_nodes)

# 计算两两最短路径
for i in tqdm(range(len(bridge_nodes))):
    for j in range(i + 1, len(bridge_nodes)):
        start = bridge_nodes[i]
        end = bridge_nodes[j]
        path, time = a_star_shortest_path(network.G, start, end)
        results[(start, end)] = (path, time)

# 输出结果到 CSV 文件
import csv

with open('bridge_shortest_paths.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Start Node", "End Node", "Path", "Total Time (hours)"])
    for (start, end), (path, time) in results.items():
        writer.writerow([start, end, str(path), time])
