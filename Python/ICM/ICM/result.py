import pandas as pd
import networkx as nx
from shapely import wkt
import geopandas as gpd
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler
import osmnx as ox
import matplotlib.pyplot as plt
from tqdm import tqdm

# 假设BPR函数中的经验参数
alpha = 0.15
beta = 4
# 单车道每小时最大通行车辆数
L = 1800
# 高峰小时系数
K = 0.1
# 高峰方向系数
D = 0.6

# ========================================读取数据==========================================#
print("开始读取数据...")
edges_all = pd.read_excel("edges_allNew.xlsx")
edges_drive = pd.read_excel("edges_driveNew.xlsx")
nodes_all = pd.read_excel("node_allNew.xlsx")
nodes_drive = pd.read_excel("node_driveNew.xlsx")

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

print("数据读取完成。")

# ============================================= 创建有向图结构 ===========================================#
print("开始创建有向图结构...")
G = nx.DiGraph()
G.graph['crs'] = 'EPSG:4326'

# 添加节点到图
def add_nodes_to_graph(nodes_df, graph):
    for _, row in tqdm(nodes_df.iterrows(), total=len(nodes_df), desc="添加节点进度"):
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
    for _, row in tqdm(edges_df.iterrows(), total=len(edges_df), desc="添加边进度"):
        start_node = row['u']
        end_node = row['v']
        edge_attributes = row.drop(['u', 'v', 'key'], errors='ignore').to_dict()
        # 解析最大速度，如果是列表，取最大值
        maxspeed = edge_attributes.get('maxspeed', 60)
        if isinstance(maxspeed, str) and '[' in maxspeed and ']' in maxspeed:
            try:
                maxspeed_list = eval(maxspeed)  # 将字符串转换为列表
                maxspeed = max(maxspeed_list)
            except (ValueError, SyntaxError):
                maxspeed = 60  # 默认值
        edge_attributes['maxspeed'] = maxspeed
        graph.add_edge(start_node, end_node, **edge_attributes)


# 添加节点
add_nodes_to_graph(nodes_all, G)
add_nodes_to_graph(nodes_drive, G)

# 添加边
add_edges_to_graph(edges_all, G)
add_edges_to_graph(edges_drive, G)

# 删除和大桥相关的边
edges_to_remove = [
    (u, v) for u, v, attrs in G.edges(data=True)
    if attrs.get("ref") == "I 695" and attrs.get("bridge") != "no" and attrs.get("bridge") != "unknown"
]

# 获取大桥相关的边的结点
start_nodes_b = [u for u, v in edges_to_remove]  # 起点列表
end_nodes_b = [v for u, v in edges_to_remove]  # 终点列表
nodes_to_remove = set(start_nodes_b + end_nodes_b)
print(f"大桥相关节点共有 {len(nodes_to_remove)} 个: {nodes_to_remove}")

G.remove_edges_from(edges_to_remove)
print("有向图结构创建完成。")

# ========================================= 使用 osmnx 求最短路径 =========================================#
print("开始使用 osmnx 求最短路径...")
# 为 osmnx 图添加边的权重（时间）
for u, v, data in G.edges(data=True):
    length = data.get('length', 1)
    maxspeed = data.get('maxspeed', 60)
    if isinstance(maxspeed, list):
        maxspeed = float(max(maxspeed))
    else:
        maxspeed = float(maxspeed)
    travel_time = length / maxspeed
    G[u][v]['travel_time'] = travel_time

# 计算大桥相关点的两两最短路径
results = {}
bridge_nodes = list(nodes_to_remove)
for i in range(len(bridge_nodes)):
    for j in range(i + 1, len(bridge_nodes)):
        start = bridge_nodes[i]
        end = bridge_nodes[j]
        try:
            path = nx.shortest_path(G, source=start, target=end, weight='travel_time')
            total_time = 0
            for k in range(len(path) - 1):
                u = path[k]
                v = path[k + 1]
                total_time += G[u][v]['travel_time']
            results[(start, end)] = (path, total_time)
        except nx.NetworkXNoPath:
            results[(start, end)] = (None, float('inf'))

# 输出结果
for (start, end), (path, time) in results.items():
    print(f"从节点 {start} 到节点 {end} 的最短路径: {path}，总时间 (小时): {time}")
print("最短路径计算完成。")

# ================================= 保存最短路径结果到文件 =================================
output_file = "shortest_paths.txt"
with open(output_file, 'w') as f:
    f.write("起点,终点,最短路径,总时间(小时)\n")
    for (start, end), (path, time) in results.items():
        path_str = str(path) if path else "无路径"
        f.write(f"{start},{end},{path_str},{time}\n")

print(f"最短路径结果已保存到 {output_file} 文件中。")

# ========================================= 流量再分配分析 =======================================#
print("开始进行流量再分配分析...")

# 假设已经有OD矩阵数据（这里需要根据实际情况获取或生成）
od_matrix = pd.DataFrame(np.random.randint(1, 100, size=(len(G.nodes), len(G.nodes))),
                         index=list(G.nodes), columns=list(G.nodes))

# 初始化边的通行能力和总通行能力
edge_capacity = {}
edge_total_capacity = {}
for node in G.nodes:
    total_cap = 0
    for _, v in G.out_edges(node):
        lane_count = G[node][v].get('lane_count', 1)
        cap = L * lane_count
        edge_capacity[(node, v)] = cap
        total_cap += cap
    edge_total_capacity[node] = total_cap

# 增量分配法参数
fractions = [0.25, 0.5, 0.25]
alternative_path_flows = {edge: 0 for edge in G.edges}

for fraction in fractions:
    for start in G.nodes:
        for end in G.nodes:
            if start != end:
                try:
                    path = nx.shortest_path(G, source=start, target=end, weight='travel_time')
                    O_i = od_matrix.loc[start, end] * fraction
                    for k in range(len(path) - 1):
                        u = path[k]
                        v = path[k + 1]
                        T_ij = edge_capacity[(u, v)]
                        alternative_path_flows[(u, v)] += O_i * (T_ij / edge_total_capacity[u])
                    # 更新边的通行时间
                    for u, v in zip(path[:-1], path[1:]):
                        length = G[u][v].get('length', 1)
                        maxspeed = G[u][v].get('maxspeed', 60)
                        free_flow_time = length / maxspeed
                        C = edge_capacity[(u, v)]
                        V = alternative_path_flows[(u, v)]
                        congestion_time = free_flow_time * (1 + alpha * (V / C) ** beta)
                        G[u][v]['travel_time'] = congestion_time
                except nx.NetworkXNoPath:
                    continue

# 计算每日高峰流量和高峰方向流量
aadts = alternative_path_flows.copy()
phvs = {edge: aadts[edge] * K for edge in G.edges}
dphv_main = {edge: phvs[edge] * D for edge in G.edges}
dphv_secondary = {edge: phvs[edge] * (1 - D) for edge in G.edges}

print("流量再分配分析完成。")

# ========================================== 拥堵点计算 =========================================#
print("开始计算拥堵点...")

congestion_points = []
for edge in G.edges:
    u, v = edge
    V = alternative_path_flows[edge]
    C = edge_capacity[edge]
    if V > C:
        congestion_points.append(edge)

print("拥堵点:", congestion_points)
print("拥堵点计算完成。")

# ========================================= 路径的交通压力（负荷度） =======================================#
print("开始计算路径的交通压力...")

traffic_loads = {}
for edge in G.edges:
    u, v = edge
    V = alternative_path_flows[edge]
    C = edge_capacity[edge]
    load = V / C
    traffic_loads[edge] = load
    if load < 1:
        status = "正常负载"
    elif load == 1:
        status = "接近饱和"
    else:
        status = "拥堵"
    print(f"边 {edge} 的负荷度: {load}，状态: {status}")

print("路径的交通压力计算完成。")

# ======================================= 拥堵对通行时间的影响 ====================================#
print("开始计算拥堵对通行时间的影响...")

congestion_times = {}
for edge in G.edges:
    u, v = edge
    length = G[u][v].get('length', 1)
    maxspeed = G[u][v].get('maxspeed', 60)
    free_flow_time = length / maxspeed
    C = edge_capacity[edge]
    V = alternative_path_flows[edge]
    if V > C:
        congestion_time = free_flow_time * (1 + alpha * (V / C) ** beta)
    else:
        congestion_time = free_flow_time
    congestion_times[edge] = congestion_time
    print(f"边 {edge} 的拥堵通行时间: {congestion_time} 小时")

print("拥堵对通行时间的影响计算完成。")

# ===================================== DBSCAN 和 K-Means 聚类===================================#
print("开始进行 DBSCAN 和 K-Means 聚类...")

# 数据预处理
def preprocess_data(nodes_df):
    nodes_df['latitude'] = nodes_df['geometry'].apply(lambda x: x.y if hasattr(x, 'y') else None)
    nodes_df['longitude'] = nodes_df['geometry'].apply(lambda x: x.x if hasattr(x, 'x') else None)
    numerical_features = nodes_df[['AADT', 'lane_count', 'AVMT']]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(numerical_features)
    return nodes_df[['latitude', 'longitude']], scaled_features

spatial_features, numerical_features = preprocess_data(gdf_nodes_all)

# 空间聚类（DBSCAN）
print("开始进行 DBSCAN 聚类...")
dbscan = DBSCAN(eps=0.001, min_samples=10)
dbscan.fit(spatial_features)
gdf_nodes_all['dbscan_cluster'] = dbscan.labels_
print("DBSCAN 聚类完成。")

# 特征聚类（K-Means）
print("开始进行 K-Means 聚类...")
unique_clusters = np.unique(dbscan.labels_)
gdf_nodes_all['kmeans_cluster'] = -1
for cluster in unique_clusters:
    if cluster != -1:
        cluster_data = numerical_features[gdf_nodes_all['dbscan_cluster'] == cluster]
        kmeans = KMeans(n_clusters=5, max_iter=300, n_init=10, init='k-means++')
        kmeans.fit(cluster_data)
        gdf_nodes_all.loc[gdf_nodes_all['dbscan_cluster'] == cluster, 'kmeans_cluster'] = kmeans.labels_
print("K-Means 聚类完成。")

# ================================= 聚类分析结果可视化 =================================
# 空间聚类结果可视化
print("开始可视化空间聚类结果...")
fig, ax = plt.subplots(figsize=(10, 10))
gdf_nodes_all.plot(ax=ax, column='dbscan_cluster', cmap='viridis', legend=True, markersize=10)
ax.set_title('空间聚类结果（DBSCAN）')
plt.show()
print("空间聚类结果可视化完成。")

# 特征聚类结果可视化
print("开始可视化特征聚类结果...")
for cluster in unique_clusters:
    if cluster != -1:
        cluster_subset = gdf_nodes_all[gdf_nodes_all['dbscan_cluster'] == cluster]
        fig, ax = plt.subplots(figsize=(8, 8))
        cluster_subset.plot(ax=ax, column='kmeans_cluster', cmap='viridis', legend=True, markersize=10)
        ax.set_title(f'特征聚类结果（K-Means） - DBSCAN 聚类 {cluster}')
        plt.show()
print("特征聚类结果可视化完成。")

# 聚类结果的利益相关者分析
stakeholder_distribution = gdf_nodes_all.groupby(['dbscan_cluster', 'kmeans_cluster']).size().reset_index(name='count')
print("不同区域内各类利益相关者在交通网络上的分布情况:")
print(stakeholder_distribution)
print("DBSCAN 和 K-Means 聚类及分析完成。")

# ===================================== 多准则决策分析模型 (MCDA) =================================#
print("开始进行多准则决策分析模型 (MCDA) 计算...")

# 定义利益相关者
stakeholders = ['居民', '企业主', '通勤者', '游客', '政府机构']

# 定义评估指标
criteria = ['通勤/物流时间', '通勤/物流/建桥/管理成本', '流量变化', '舒适性（道路负荷度）']

# 手动为每类利益相关者构建判断矩阵
judgment_matrices = {
    '居民': np.array([
        [1, 3, 5, 2],
        [1 / 3, 1, 3, 1 / 2],
        [1 / 5, 1 / 3, 1, 1 / 4],
        [1 / 2, 2, 4, 1]
    ]),
    '企业主': np.array([
        [1, 1 / 3, 5, 1 / 2],
        [3, 1, 7, 2],
        [1 / 5, 1 / 7, 1, 1 / 4],
        [2, 1 / 2, 4, 1]
    ]),
    '通勤者': np.array([
        [1, 3, 3, 2],
        [1 / 3, 1, 1, 1 / 2],
        [1 / 3, 1, 1, 1 / 4],
        [1 / 2, 2, 4, 1]
    ]),
    '游客': np.array([
        [1, 1 / 3, 1 / 5, 1 / 2],
        [3, 1, 1 / 3, 2],
        [5, 3, 1, 4],
        [2, 1 / 2, 1 / 4, 1]
    ]),
    '政府机构': np.array([
        [1, 3, 5, 2],
        [1 / 3, 1, 3, 1 / 2],
        [1 / 5, 1 / 3, 1, 1 / 4],
        [1 / 2, 2, 4, 1]
    ])
}


# 计算判断矩阵的权重和一致性比例
def calculate_weights_and_CR(judgment_matrix):
    n = len(judgment_matrix)
    # 归一化每列
    norm_matrix = judgment_matrix / judgment_matrix.sum(axis=0)
    # 计算权重
    weights = norm_matrix.mean(axis=1)
    # 计算特征值和特征向量
    eigen_values, _ = np.linalg.eig(judgment_matrix)
    max_eigen_value = np.max(eigen_values)
    # 计算一致性指标 CI
    CI = (max_eigen_value - n) / (n - 1)
    # 随机一致性指标 RI
    RI = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45]
    # 计算一致性比例 CR
    CR = CI / RI[n - 1]
    return weights, CR


# 计算每类利益相关者的指标权重和一致性比例
weights = {}
CR_values = {}
with tqdm(total=len(stakeholders), desc="计算判断矩阵权重和CR进度") as pbar:
    for stakeholder, matrix in judgment_matrices.items():
        w, cr = calculate_weights_and_CR(matrix)
        weights[stakeholder] = w
        CR_values[stakeholder] = cr

        # 输出每类利益相关者的判断矩阵、权重和一致性比例
        print(f"{stakeholder} 的判断矩阵：")
        print(pd.DataFrame(matrix, index=criteria, columns=criteria))
        print(f"{stakeholder} 的指标权重：{w}")
        print(f"{stakeholder} 的一致性比例 CR：{cr}")
        if cr < 0.1:
            print(f"{stakeholder} 的判断矩阵通过一致性检验。")
        else:
            print(f"{stakeholder} 的判断矩阵未通过一致性检验，请重新调整。")
        pbar.update(1)

# 假设每个利益相关者的相对重要性权重（这里简单假设都相等，
# 实际应用中，这需要根据具体情况，如利益相关者的影响力、对决策的参与度等因素确定）
stakeholder_importance = {
    '居民': 0.2,
    '企业主': 0.2,
    '通勤者': 0.2,
    '游客': 0.2,
    '政府机构': 0.2
}

# 计算综合指标权重
composite_weights = np.zeros(len(criteria))
for stakeholder in stakeholders:
    composite_weights += stakeholder_importance[stakeholder] * weights[stakeholder]

print("\n综合指标权重：")
for i, criterion in enumerate(criteria):
    print(f"{criterion}: {composite_weights[i]}")

# 假设存在一个数据矩阵，代表大桥倒塌后各利益相关者在各指标上的量化影响值
# 这里随机生成示例数据，在实际使用时，需要通过调研、数据分析等方式获取真实数据
impact_data = {
    '居民': np.random.rand(len(criteria)),
    '企业主': np.random.rand(len(criteria)),
    '通勤者': np.random.rand(len(criteria)),
    '游客': np.random.rand(len(criteria)),
    '政府机构': np.random.rand(len(criteria))
}

# 计算每个利益相关者的影响得分
stakeholder_scores = {}
with tqdm(total=len(stakeholders), desc="计算利益相关者影响得分进度") as pbar:
    for stakeholder in stakeholders:
        scores = impact_data[stakeholder] * weights[stakeholder]
        stakeholder_scores[stakeholder] = scores.sum()
        pbar.update(1)

# 计算综合影响得分
composite_score = 0
for stakeholder in stakeholders:
    composite_score += stakeholder_importance[stakeholder] * stakeholder_scores[stakeholder]

print("\n各利益相关者的影响得分：")
for stakeholder, score in stakeholder_scores.items():
    print(f"{stakeholder}: {score}")

print(f"\n大桥倒塌对利益相关者的综合影响得分: {composite_score}")

# 以下是一个更详细的结果解读示例
if composite_score > 0.7:
    print("大桥倒塌对利益相关者的综合影响非常大，必须立即采取全面且有力的措施来应对。")
elif 0.5 < composite_score <= 0.7:
    print("大桥倒塌对利益相关者的综合影响较大，需要重点关注并制定针对性的解决方案。")
elif 0.3 < composite_score <= 0.5:
    print("大桥倒塌对利益相关者有一定影响，应持续跟踪并适时采取措施。")
else:
    print("大桥倒塌对利益相关者的综合影响相对较小，但仍需保持关注，以防情况变化。")
print("多准则决策分析模型 (MCDA) 计算完成。")

# ================================= 多目标规划模型 (MOP) =================================
import cvxpy as cp

print("开始进行多目标规划模型 (MOP) 计算...")

# 设定多个目标函数的权重（这里简单假设相等，实际可根据需求调整）
w1 = 0.3
w2 = 0.3
w3 = 0.4

# 定义变量
# 假设每个边有一个是否开放的二进制变量
x = {edge: cp.Variable(boolean=True) for edge in G.edges}

# 目标函数 1: 交通拥堵延迟时间最小化
# 假设拥堵延迟时间可以通过各边的拥堵时间加权和表示
delay_times = {
    edge: congestion_times[edge] - (G[edge[0]][edge[1]].get('length', 1) / G[edge[0]][edge[1]].get('maxspeed', 60))
    for edge in G.edges}
f1 = cp.sum([x[edge] * delay_times[edge] for edge in G.edges])

# 目标函数 2: 重建成本最小化
# 假设每条边有一个重建成本（这里简单随机生成，实际需根据真实数据）
reconstruction_costs = {edge: np.random.randint(1000, 10000) for edge in G.edges}
f2 = cp.sum([x[edge] * reconstruction_costs[edge] for edge in G.edges])

# 目标函数 3: 利益相关者的不满值最小化
# 假设利益相关者不满值可以根据各边流量和通行能力关系计算
dissatisfaction = {edge: max(0, alternative_path_flows[edge] - edge_capacity[edge]) for edge in G.edges}
f3 = cp.sum([x[edge] * dissatisfaction[edge] for edge in G.edges])

# 总目标函数：加权和
objective = cp.Minimize(w1 * f1 + w2 * f2 + w3 * f3)

# 约束条件
# 1. 替代路径的通行能力约束
# 假设总通行能力有一个上限（这里简单设为一个固定值，实际需根据情况确定）
total_capacity_limit = 10000
constraints = [cp.sum([x[edge] * edge_capacity[edge] for edge in G.edges]) <= total_capacity_limit]

# 2. 预算限制（假设预算为一个固定值）
budget_limit = 50000
constraints.append(cp.sum([x[edge] * reconstruction_costs[edge] for edge in G.edges]) <= budget_limit)

# 构建问题并求解
prob = cp.Problem(objective, constraints)
prob.solve()

# 输出结果
print(f"优化目标值: {prob.value}")
optimal_edges = [edge for edge in G.edges if x[edge].value == 1]
print("最优开放的边:", optimal_edges)
print("多目标规划模型 (MOP) 计算完成。")
