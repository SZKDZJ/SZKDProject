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


# 假设BPR函数中的经验参数
alpha = 0.15
beta = 4


#========================================读取数据==========================================#
edges_all = pd.read_excel("edges_allNew.xlsx")
edges_drive = pd.read_excel("edges_driveNew.xlsx")

# 读取 Excel 文件中的所有工作表
file_path1 = "/Users/eureka/PycharmProjects/ICM/node_allNew.xlsx"
xls1 = pd.ExcelFile(file_path1)
# 读取所有工作表的数据，并将其合并为一个 DataFrame
nodes_all = pd.concat([xls1.parse(sheet) for sheet in xls1.sheet_names], ignore_index=True)

# 读取 Excel 文件中的所有工作表
file_path2 = "/Users/eureka/PycharmProjects/ICM/node_driveNew.xlsx"
xls2 = pd.ExcelFile(file_path2)
# 读取所有工作表的数据，并将其合并为一个 DataFrame
nodes_drive = pd.concat([xls2.parse(sheet) for sheet in xls2.sheet_names], ignore_index=True)

# 将 WKT 字段解析为几何对象
edges_all['geometry'] = edges_all['geometry'].apply(wkt.loads)
edges_drive['geometry'] = edges_drive['geometry'].apply(wkt.loads)
nodes_all['geometry'] = nodes_all['geometry'].apply(wkt.loads)
nodes_drive['geometry'] = nodes_drive['geometry'].apply(wkt.loads)

# 将 edges 和 nodes 转换为 GeoDataFrame
gdf_edges_all = gpd.GeoDataFrame(edges_all, geometry='geometry')
gdf_edges_drive = gpd.GeoDataFrame(edges_drive, geometry='geometry')
gdf_nodes_all = gpd.GeoDataFrame(nodes_all, geometry='geometry')
gdf_nodes_drive = gpd.GeoDataFrame(nodes_drive, geometry='geometry')

# 确保设置正确的坐标参考系统（CRS），使用的是 WGS84 坐标系（EPSG:4326）
gdf_edges_all.set_crs("EPSG:4326", allow_override=True, inplace=True)
gdf_edges_drive.set_crs("EPSG:4326", allow_override=True, inplace=True)
gdf_nodes_all.set_crs("EPSG:4326", allow_override=True, inplace=True)
gdf_nodes_drive.set_crs("EPSG:4326", allow_override=True, inplace=True)

# 执行空间连接
nodes_with_edges_all = gpd.sjoin(gdf_nodes_all, gdf_edges_all, how="left", predicate='intersects')
nodes_with_edges_drive = gpd.sjoin(gdf_nodes_drive, gdf_edges_drive, how="left", predicate='intersects')

# 检查连接结果
print(nodes_with_edges_all.head())
print(nodes_with_edges_drive.head())

'''
#=====================================使用 matplotlib 绘制边和节点数据======================================#
fig, ax = plt.subplots(figsize=(50, 50))

# 选择一个seaborn的颜色调色板
blue_color_palette = sns.color_palette("Blues", n_colors=3)
red_color_palette = sns.color_palette("Reds", n_colors=3)

# 绘制边数据
gdf_edges_all.plot(ax=ax, color='skyblue', alpha=0.5, linewidth=0.8, label='Edges All')
gdf_edges_drive.plot(ax=ax, color='salmon', alpha=0.5, linewidth=0.8, label='Edges Drive')

# 绘制节点数据，减少大小和透明度
gdf_nodes_all.plot(ax=ax, color=blue_color_palette[1], marker='o', label='Nodes All', alpha=0.8, markersize=4)
gdf_nodes_drive.plot(ax=ax, color=red_color_palette[1], marker='o', label='Nodes Drive', alpha=0.8, markersize=4)

# 添加图例
ax.legend()
plt.savefig("map.png")
# 显示图形
plt.show()
'''
#============================================== 连通性判断函数 ============================================#
class UnionFind:
    def __init__(self, n):
        # 初始化父节点数组和树的大小数组
        self.parent = list(range(n))
        self.size = [1] * n  # 记录每个集合的大小，用于优化合并操作

    def find(self, x):
        # 查找并且路径压缩
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        # 合并操作，按大小合并
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX != rootY:
            # 将小的集合合并到大的集合
            if self.size[rootX] < self.size[rootY]:
                rootX, rootY = rootY, rootX
            self.parent[rootY] = rootX
            self.size[rootX] += self.size[rootY]

    def connected(self, x, y):
        return self.find(x) == self.find(y)


#============================================ 创建有向图结构 ===========================================#

G = nx.DiGraph()

# 添加节点到图
def add_nodes_to_graph(nodes_df, graph):
    for _, row in nodes_df.iterrows():
        node_id = row['osmid']
        node_attributes = {
            'highway': row.get('highway', None),
            'ref': row.get('ref', None),
            'street_count': row.get('street_count', None),
            'junction': row.get('junction', None),
            'railway': row.get('railway', None),
            'geometry': row.get('geometry', None)
        }
        graph.add_node(node_id, **node_attributes)

# 添加边到图
def add_edges_to_graph(edges_df, graph):
    for _, row in edges_df.iterrows():
        start_node = row['u']
        end_node = row['v']
        edge_attributes = row.drop(['u', 'v', 'key'], errors='ignore').to_dict()
        # 解析最大速度，如果是列表，取最大值
        maxspeed = edge_attributes.get('maxspeed',25)
        if isinstance(maxspeed, str) and '[' in maxspeed and ']' in maxspeed:
            try:
                maxspeed_list = ast.literal_eval(maxspeed)  # 将字符串转换为列表
                maxspeed = max(maxspeed_list)
            except (ValueError, SyntaxError):
                maxspeed = 25  # 默认值
        edge_attributes['maxspeed'] = maxspeed
        graph.add_edge(start_node, end_node, **edge_attributes)
'''
# 添加节点
def add_nodes_to_graph(nodes_df, graph):
    for _, row in nodes_df.iterrows():
        node_id = row['osmid']
        geometry = row['geometry'] if pd.notna(row['geometry']) else None
        node_attributes = {
            'highway': row.get('highway', None),
            'ref': row.get('ref', None),
            'street_count': row.get('street_count', None),
            'junction': row.get('junction', None),
            'railway': row.get('railway', None),
            'geometry': geometry
        }
        graph.add_node(node_id, **node_attributes)

add_nodes_to_graph(nodes_all, G)
add_nodes_to_graph(nodes_drive, G)

# 添加边
def add_edges_to_graph(edges_df, graph):
    for _, row in edges_df.iterrows():
        start_node = row['u']
        end_node = row['v']
        if start_node not in graph.nodes:
            graph.add_node(start_node)
        if end_node not in graph.nodes:
            graph.add_node(end_node)
        edge_attributes = row.drop(['u', 'v', 'key'], errors='ignore').to_dict()
        graph.add_edge(start_node, end_node, **edge_attributes)

add_edges_to_graph(edges_all, G)
add_edges_to_graph(edges_drive, G)

# 删除和大桥相关的边
edges_to_remove = [
    (u, v) for u, v, attrs in G.edges(data=True)
    if attrs.get("ref") == "I 695" and attrs.get("bridge") != "no" and attrs.get("bridge") != "unknown"
]

# 获取大桥相关的边的结点
start_nodes_b = [u for u, v in edges_to_remove]  # 起点列表
end_nodes_b = [v for u, v in edges_to_remove]    # 终点列表
nodes_to_remove = set(start_nodes_b + end_nodes_b)
print(f"大桥相关节点共有 {len(nodes_to_remove)} 个: {nodes_to_remove}")

G.remove_edges_from(edges_to_remove)
'''



#============================================= 并查集判断连通性 ===========================================#
'''
# 假设每个节点的OSM ID是唯一的，创建节点索引的映射
node_index = {node_id: idx for idx, node_id in enumerate(G.nodes)}

# 初始化并查集
uf = UnionFind(len(G.nodes))

# 遍历每一条边，进行并查集的union操作
for _, row in edges_all.iterrows():
    start_node = row['u']
    end_node = row['v']

    # 获取节点在图中的索引
    start_idx = node_index[start_node]
    end_idx = node_index[end_node]

    # 使用并查集的union操作合并节点
    uf.union(start_idx, end_idx)

for _, row in edges_drive.iterrows():
    start_node = row['u']
    end_node = row['v']

    # 获取节点在图中的索引
    start_idx = node_index[start_node]
    end_idx = node_index[end_node]

    # 使用并查集的union操作合并节点
    uf.union(start_idx, end_idx)

# 判断图是否连通
# 检查图中是否所有节点都在同一个集合中
is_connected = True
first_node = list(G.nodes)[0]
first_idx = node_index[first_node]

# 检查每个节点是否与第一个节点连通
for node in G.nodes:
    if uf.find(first_idx) != uf.find(node_index[node]):
        is_connected = False
        break

print("Graph is connected:", is_connected)
'''
#========================================= A*最优路径 =========================================#

def a_star_shortest_path(graph, start, end):
    """
    使用 A* 算法计算最短路径
    :param graph: NetworkX 图对象
    :param start: 起点节点 ID
    :param end: 终点节点 ID
    :return: 最短路径和路径总时间
    """
    # 初始化优先队列
    open_set = []
    heapq.heappush(open_set, (0, start))  # (f(n), 节点)

    # 路径记录
    came_from = {}

    # g(n): 起点到当前节点的实际代价（时间）
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start] = 0

    # f(n): 起点到终点的估计代价
    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start] = heuristic_cost_estimate(graph, start, end)

    while open_set:
        _, current = heapq.heappop(open_set)  # 取出 f(n) 最小的节点

        # 如果到达终点，构造路径
        if current == end:
            return reconstruct_path(came_from, current), g_score[current]

        # 遍历当前节点的邻居
        for neighbor in graph.neighbors(current):
            # 获取边的长度和最大速度
            edge_data = graph[current][neighbor]
            edge_length = edge_data.get('length', 1)
            edge_speed = edge_data.get('maxspeed')  # 获取最大速度

            # 如果 maxspeed 是列表（例如 [30, 50]），取最大值并转换为浮动数值
            if isinstance(edge_speed, list):
                edge_speed = float(max(edge_speed))
            else:
                edge_speed = float(edge_speed)  # 确保它是浮动数值

            # 计算通过当前节点到邻居节点的 g 值
            tentative_g_score = g_score[current] + edge_length / edge_speed

            if tentative_g_score < g_score[neighbor]:
                # 更新路径记录
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic_cost_estimate(graph, neighbor, end)

                # 如果邻居不在 open_set 中，将其添加
                if not any(neighbor == item[1] for item in open_set):
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None, float('inf')  # 如果没有路径，则返回 None 和无限代价

def heuristic_cost_estimate(graph, node, goal):
    """
    启发式函数，估计从当前节点到终点的时间代价
    :param graph: NetworkX 图对象
    :param node: 当前节点 ID
    :param goal: 终点节点 ID
    :return: 启发式代价（时间）
    """
    # 获取当前节点和目标节点的几何位置（假设是经纬度）
    node_pos = graph.nodes[node].get('geometry')
    goal_pos = graph.nodes[goal].get('geometry')

    if node_pos and goal_pos:
        # 将 Shapely 的 Point 转换为经纬度元组
        node_coords = (node_pos.y, node_pos.x)  # 假设 node_pos 是 Point 对象
        goal_coords = (goal_pos.y, goal_pos.x)  # 假设 goal_pos 是 Point 对象

        # 使用 geopy 来计算经纬度之间的球面距离（单位：公里）
        distance = geodesic(node_coords, goal_coords).kilometers
        return distance  # 返回距离作为估计代价

    return float('inf')

# 重建路径
def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]

# 添加节点和边
add_nodes_to_graph(nodes_all, G)
add_edges_to_graph(edges_all, G)

# 删除大桥相关的边
edges_to_remove = [
    (u, v) for u, v, attrs in G.edges(data=True)
    if attrs.get("ref") == "I 695" and attrs.get("bridge") != "no" and attrs.get("bridge") != "unknown"
]
G.remove_edges_from(edges_to_remove)

# 获取大桥相关的节点
start_nodes_b = [u for u, v in edges_to_remove]
end_nodes_b = [v for u, v in edges_to_remove]
bridge_nodes = set(start_nodes_b + end_nodes_b)

# 计算大桥相关点的两两最短路径
results = {}
bridge_nodes = list(bridge_nodes)
for i in range(len(bridge_nodes)):
    for j in range(i + 1, len(bridge_nodes)):
        start = bridge_nodes[i]
        end = bridge_nodes[j]
        path, time = a_star_shortest_path(G, start, end)
        results[(start, end)] = (path, time)

# 输出结果
for (start, end), (path, time) in results.items():
    print(f"从节点 {start} 到节点 {end} 的最短路径: {path}，总时间 (小时): {time}")


#======================================== 流量再分配分析 =======================================#
def calculate_alternative_path_flow(od_matrix, capacity, total_capacity):
    """
    计算替代路径流量
    :param od_matrix: OD矩阵，表示起点到终点的流量需求
    :param capacity: 某条替代路径的通行能力
    :param total_capacity: 所有替代路径的通行能力总和
    :return: 该替代路径的流量
    """
    return od_matrix * capacity / total_capacity


# 假设已经有OD矩阵数据（这里需要根据实际情况获取或生成）
od_matrix = pd.DataFrame(np.random.randint(1, 100, size=(len(G.nodes), len(G.nodes))),
                         index=list(G.nodes), columns=list(G.nodes))

# 计算每条边的替代路径流量
edge_capacity = defaultdict(lambda: 100)  # 假设每条边的通行能力，需根据实际情况调整
edge_total_capacity = defaultdict(lambda: 1000)  # 假设所有可达替代路径的通行能力总和，需根据实际情况调整
alternative_path_flows = {}
for edge in G.edges:
    start, end = edge
    alternative_path_flows[edge] = calculate_alternative_path_flow(od_matrix[start][end],
                                                                 edge_capacity[edge],
                                                                 edge_total_capacity[start])

#========================================= 拥堵点计算 =========================================#
def calculate_congestion_points(edges_df, flow_data):
    """
    计算拥堵点
    :param edges_df: 包含路段信息的DataFrame
    :param flow_data: 路段流量数据
    :return: 拥堵点列表
    """
    congestion_points = []
    for _, row in edges_df.iterrows():
        start_node = row['u']
        end_node = row['v']
        edge_flow = flow_data.get((start_node, end_node), 0)
        # 假设路段通行能力计算公式，需根据实际情况调整
        capacity = 1800 * row.get('lane_count', 1)
        if edge_flow > capacity:
            congestion_points.append((start_node, end_node))
    return congestion_points


congestion_points = calculate_congestion_points(edges_all, alternative_path_flows)
print("拥堵点:", congestion_points)

#======================================== 路径的交通压⼒ =======================================#
def calculate_path_traffic_pressure(path, flow_data):
    """
    计算路径的交通压力
    :param path: 路径节点列表
    :param flow_data: 路段流量数据
    :return: 路径的交通压力值
    """
    traffic_pressure = 0
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        edge_flow = flow_data.get((start, end), 0)
        traffic_pressure += edge_flow
    return traffic_pressure

# 计算之前得到的最短路径的交通压力
for (start, end), (path, _) in results.items():
    traffic_pressure = calculate_path_traffic_pressure(path, alternative_path_flows)
    print(f"从节点 {start} 到节点 {end} 的最短路径的交通压力: {traffic_pressure}")
#====================================== 拥堵对通⾏时间的影响 ====================================#

def calculate_congestion_time(edges_df, flow_data):
    """
    计算拥堵情况下的通行时间
    :param edges_df: 包含路段信息的DataFrame
    :param flow_data: 路段流量数据
    :return: 包含路段及其拥堵通行时间的字典
    """
    congestion_times = {}
    for _, row in edges_df.iterrows():
        start_node = row['u']
        end_node = row['v']
        edge_flow = flow_data.get((start_node, end_node), 0)
        # 假设自由流通行时间的计算方式（需根据实际情况调整）
        free_flow_time = row.get('length', 1) / row.get('maxspeed', 60)
        capacity = 1800 * row.get('lane_count', 1)
        if edge_flow > capacity:
            # 使用BPR函数计算拥堵通行时间
            congestion_time = free_flow_time * (1 + alpha * (edge_flow / capacity) ** beta)
        else:
            congestion_time = free_flow_time
        congestion_times[(start_node, end_node)] = congestion_time
    return congestion_times


congestion_times = calculate_congestion_time(edges_all, alternative_path_flows)
# 输出部分拥堵时间结果示例
sample_edges = list(congestion_times.keys())[:5]
for edge in sample_edges:
    print(f"边 {edge} 的拥堵通行时间: {congestion_times[edge]} 小时")

#==================================== DBSCAN 和 K-Means 聚类===================================#
# 数据预处理，提取经纬度坐标作为DBSCAN的输入
def preprocess_data(nodes_df):
    nodes_df['latitude'] = nodes_df['geometry'].apply(lambda x: x.y if isinstance(x, Point) else None)
    nodes_df['longitude'] = nodes_df['geometry'].apply(lambda x: x.x if isinstance(x, Point) else None)
    return nodes_df[['latitude', 'longitude']]


preprocessed_data = preprocess_data(gdf_nodes_all)
# 进行DBSCAN聚类
dbscan = DBSCAN(eps=0.001, min_samples=10)
dbscan.fit(preprocessed_data)
gdf_nodes_all['dbscan_cluster'] = dbscan.labels_

# 对每个DBSCAN聚类结果进行K-Means聚类细分
unique_clusters = np.unique(dbscan.labels_)
for cluster in unique_clusters:
    if cluster != -1:
        cluster_data = preprocessed_data[gdf_nodes_all['dbscan_cluster'] == cluster]
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(cluster_data)
        kmeans = KMeans(n_clusters=6, max_iter=300, n_init=10, init='k-means++')
        kmeans.fit(scaled_data)
        gdf_nodes_all.loc[gdf_nodes_all['dbscan_cluster'] == cluster, 'kmeans_cluster'] = kmeans.labels_


# 分析聚类结果，输出不同区域内各类利益相关者在交通网络上的分布情况
stakeholder_distribution = gdf_nodes_all.groupby(['dbscan_cluster', 'kmeans_cluster']).size().reset_index(name='count')
print("不同区域内各类利益相关者在交通网络上的分布情况:")
print(stakeholder_distribution)



#=============================== 多准则决策分析模型 (MCDA) 和 层次分析法 (AHP) =================================#
# 定义利益相关者及其评估指标（量化）
stakeholders = ['城市居民', '企业主', '郊区居民和通勤者', '游客', '政府机构']
criteria = ['通勤/物流时间', '通勤/物流/建桥成本', '环境影响']
# 构建判断矩阵（这里随机生成示例数据，需根据实际情况调整）
def build_judgment_matrix(criteria):
    num_criteria = len(criteria)
    matrix = np.ones((num_criteria, num_criteria))
    for i in range(num_criteria):
        for j in range(i + 1, num_criteria):
            matrix[i][j] = np.random.randint(1, 9)
            matrix[j][i] = 1 / matrix[i][j]
    return matrix


judgment_matrices = {stakeholder: build_judgment_matrix(criteria) for stakeholder in stakeholders}

# 归一化每列，计算每个指标的权重
def calculate_weights(judgment_matrix):
    norm_matrix = judgment_matrix / judgment_matrix.sum(axis=0)
    weights = norm_matrix.mean(axis=1)
    return weights


weights = {stakeholder: calculate_weights(judgment_matrices[stakeholder]) for stakeholder in stakeholders}

# 一致性检验（计算一致性比例CR）
def consistency_ratio(judgment_matrix):
    n = len(judgment_matrix)
    eigen_values, _ = np.linalg.eig(judgment_matrix)
    max_eigen_value = np.max(eigen_values)
    CI = (max_eigen_value - n) / (n - 1)
    RI = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45]
    CR = CI / RI[n - 1]
    return CR


consistency_check = {stakeholder: consistency_ratio(judgment_matrices[stakeholder]) for stakeholder in stakeholders}
for stakeholder, cr in consistency_check.items():
    if cr < 0.1:
        print(f"{stakeholder} 的判断矩阵通过一致性检验，CR值为: {cr}")
    else:
        print(f"{stakeholder} 的判断矩阵未通过一致性检验，CR值为: {cr}")


# 多目标规划模型 (MOP) 部分
# 假设每个目标函数对应的影响值（倒塌后的影响值、重建后的影响值）（随机生成示例数据，需根据实际情况调整）
def generate_mop_data(stakeholders, criteria):
    mop_data = defaultdict(dict)
    for stakeholder in stakeholders:
        for criterion in criteria:
            mop_data[stakeholder][criterion] = {
                '倒塌后': np.random.rand(),
                '重建后': np.random.rand()
            }
    return mop_data


mop_data = generate_mop_data(stakeholders, criteria)

# 计算每个准则的总权重贡献度并进行加权计算，判断是否重建大桥
def make_decision(stakeholders, criteria, weights, mop_data):
    total_weights = {criterion: sum(weights[stakeholder][i] for stakeholder, i in zip(stakeholders, range(len(criteria))))
                     for criterion in criteria}
    collapse_score = 0
    rebuild_score = 0
    for criterion in criteria:
        collapse_score += total_weights[criterion] * sum(mop_data[stakeholder][criterion]['倒塌后'] for stakeholder in stakeholders)
        rebuild_score += total_weights[criterion] * sum(mop_data[stakeholder][criterion]['重建后'] for stakeholder in stakeholders)
    if collapse_score > rebuild_score:
        decision = '重建大桥'
    else:
        decision = '不重建大桥'
    return decision


decision = make_decision(stakeholders, criteria, weights, mop_data)
print(f"综合决策结果: {decision}")
