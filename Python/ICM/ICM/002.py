import numpy as np
import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt
from shapely import wkt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from pulp import LpMaximize, LpProblem, LpVariable, lpSum
from shapely.geometry import Point
import geopandas as gpd
# 常量：需要移除的大桥标识
BRIDGE_REF = "I 695"

# ============================ 读取数据 ============================ #
def load_aadt(path):
    print("Loading AADT data...")
    """加载流量数据"""
    try:
        df = pd.read_csv(path, encoding='utf-8-sig')
        df.columns = df.columns.str.strip().str.lower().str.replace(r'[^\w]', '_', regex=True).str.replace(r'_+', '_', regex=True)

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
aadt_data = load_aadt("MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.csv")

# 读取所有节点和边的数据
def read_edges_and_nodes(files):
    """读取多个 Excel 文件并返回合并后的 DataFrame"""
    return pd.concat([pd.read_excel(file) for file in files], ignore_index=True)


edges_all = read_edges_and_nodes(["edges_allNew.xlsx"])
edges_drive = read_edges_and_nodes(["edges_driveNew.xlsx"])
nodes_all = read_edges_and_nodes(["node_allNew.xlsx"])
nodes_drive = read_edges_and_nodes(["node_driveNew.xlsx"])

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
        def build_network(self, nodes_gdf, edges_gdf, aadt_df):
            print("Building network...")
            # 添加节点，并确保 street_count 属性包含在结点属性中
            for _, row in nodes_gdf.iterrows():
                self.G.add_node(
                    row['osmid'],
                    pos=(row['geometry'].x, row['geometry'].y),
                    street_count=row.get('street_count', 0),  # 添加 street_count 属性
                    **row.drop(['geometry', 'osmid']).to_dict()
                )

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
            'ref': row.get('ref', ''),
            'highway': row.get('highway', 'unknown')  # 添加 highway 属性
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

# ============================ 公交网络============================ #
import geopandas as gpd
from shapely.geometry import Point

# 加载数据
bus_routes = pd.read_excel("Bus_RoutesNew.xlsx")
bus_stops = pd.read_excel("bus_stopNew.xlsx")

# 清理列名并规范为小写
bus_stops.columns = bus_stops.columns.str.strip().str.lower()
bus_routes.columns = bus_routes.columns.str.strip().str.lower()

# 转换公交站点为 GeoDataFrame
bus_stops['geometry'] = bus_stops.apply(lambda row: Point(row['x'], row['y']), axis=1)
gdf_bus_stops = gpd.GeoDataFrame(bus_stops, geometry='geometry', crs="EPSG:4326")


class BusNetwork:
    def __init__(self):
        self.G_bus = nx.DiGraph()  # 使用有向图表示公交网络

    def build_bus_network(self, bus_routes_df, bus_stops_df):
        print("Building bus network...")

        # 添加公交站点
        for _, row in bus_stops_df.iterrows():
            try:
                stop_id = row['stop_id']
                self.G_bus.add_node(
                    stop_id,
                    pos=(row['x'], row['y']),
                    stop_name=row['stop_name'],
                    rider_on=row['rider_on'],
                    rider_off=row['rider_off'],
                    rider_total=row['rider_tota'],
                    shelter=row['shelter'],
                    county=row['county'],
                    routes_served=row['routes_ser'],
                    mode=row['mode']
                )
            except KeyError as e:
                print(f"Skipping row with missing column: {e}, row: {row}")
                continue

        # 为每条路线建立边
        for _, row in bus_routes_df.iterrows():
            route_name = row['route_name']
            route_type = row['route_type']
            shape_length = row['shape__length']

            # 获取所有服务该路线的站点
            route_stops = bus_stops_df[bus_stops_df['routes_ser'].str.contains(route_name, na=False)]

            # 按 stop_id 排序
            route_stops = route_stops.sort_values('stop_id')
            stops = route_stops['stop_id'].tolist()

            # 添加边：按顺序添加相邻站点之间的边
            for u, v in zip(stops[:-1], stops[1:]):
                if self.G_bus.has_node(u) and self.G_bus.has_node(v):
                    self.G_bus.add_edge(
                        u, v,
                        route_name=route_name,
                        route_type=route_type,
                        shape_length=shape_length
                    )

    def plot_network(self):
        print("Plotting bus network...")
        pos = {node: (data['pos'][0], data['pos'][1]) for node, data in self.G_bus.nodes(data=True)}
        plt.figure(figsize=(12, 8))
        nx.draw(
            self.G_bus, pos,
            node_size=20,
            edge_color="blue",
            width=2,  # 设置边的宽度
            with_labels=False,
            node_color="red"
        )
        plt.title("Bus Network Visualization")
        plt.show()


# 实例化并构建公交网络
bus_network = BusNetwork()
bus_network.build_bus_network(bus_routes, gdf_bus_stops)

# 可视化
bus_network.plot_network()

# ============================ 站点覆盖率计算 ============================ #
def euclidean_distance(node1, node2):
    return np.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)


def calculate_coverage(nodes, bus_stations, max_distance):
    """计算总覆盖率和盲区节点"""
    covered_nodes = set()
    for station_id, station_data in bus_stations.items():
        station_pos = station_data['pos']
        for node_id, node_data in nodes.items():
            if euclidean_distance(node_data['pos'], station_pos) <= max_distance:
                covered_nodes.add(node_id)

    uncovered_nodes = [node for node in nodes if node not in covered_nodes]
    total_coverage = len(covered_nodes) / len(nodes)
    return total_coverage, uncovered_nodes


# ============================ 新增站点选址优化 ============================ #
def ahp_weights(comparison_matrix):
    n = comparison_matrix.shape[0]
    eigenvalues, eigenvectors = np.linalg.eig(comparison_matrix)
    max_eigenvalue = np.max(eigenvalues)
    weights = eigenvectors[:, np.argmax(eigenvalues)].real
    weights = weights / weights.sum()
    consistency_index = (max_eigenvalue - n) / (n - 1)
    random_index = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.9, 5: 1.12}
    cr = consistency_index / random_index.get(n, 1.49)
    if cr >= 0.1:
        raise ValueError("Consistency Ratio exceeds acceptable threshold.")
    return weights


comparison_matrix = np.array([
    [1, 3, 5],
    [1 / 3, 1, 2],
    [1 / 5, 1 / 2, 1]
])
weights = ahp_weights(comparison_matrix)


# 聚类未覆盖区域
def cluster_uncovered_nodes(uncovered_nodes, nodes, eps=0.01, min_samples=2):
    positions = np.array([nodes[node]['pos'] for node in uncovered_nodes])
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(positions)
    clusters = {}
    for node, cluster_id in zip(uncovered_nodes, clustering.labels_):
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        clusters[cluster_id].append(node)
    return clusters


# ============================ 整数规划站点选址 ============================ #
def optimize_station_locations(nodes, demand_intensity, budget, service_radius, candidate_stations):
    model = LpProblem("Station_Location_Optimization", LpMaximize)

    x = {node: LpVariable(f"x_{node}", cat="Binary") for node in nodes}
    y = {station: LpVariable(f"y_{station}", cat="Binary") for station in candidate_stations}

    model += lpSum(demand_intensity[node] * x[node] for node in nodes), "Maximize Coverage"

    for node in nodes:
        model += lpSum(y[station] for station in candidate_stations if
                       euclidean_distance(nodes[node]['pos'], candidate_stations[station]['pos']) <= service_radius) >= \
                 x[node]

    model += lpSum(y[station] for station in candidate_stations) <= budget, "Budget Constraint"

    model.solve()

    selected_stations = [station for station in candidate_stations if y[station].varValue == 1]
    return selected_stations


# ============================ 优化路线生成 ============================ #
def generate_routes(graph, selected_stations):
    routes = []
    for station in selected_stations:
        shortest_path = nx.shortest_path(graph, source=station, weight='length')
        routes.append(shortest_path)
    return routes


# ============================ 优化频率与排队论 ============================ #
def optimize_frequency(demand, capacity, cost_weight=1):
    frequency = demand / capacity
    waiting_time_cost = 1 / (2 * frequency)
    operating_cost = frequency * cost_weight
    total_cost = waiting_time_cost + operating_cost
    return frequency, total_cost


# ============================ 主程序 ============================ #
# 站点与节点数据示例
nodes = {i: {'pos': (np.random.rand(), np.random.rand())} for i in range(100)}
bus_stations = {i: {'pos': (np.random.rand(), np.random.rand())} for i in range(10)}

# 计算覆盖率
max_distance = 0.01
coverage, uncovered_nodes = calculate_coverage(nodes, bus_stations, max_distance)
print(f"Initial Coverage: {coverage}")

# 聚类未覆盖区域
clusters = cluster_uncovered_nodes(uncovered_nodes, nodes)
print(f"Clusters: {clusters}")

# 整数规划选址
candidate_stations = {i: {'pos': (np.random.rand(), np.random.rand())} for i in range(20)}
demand_intensity = {i: np.random.randint(1, 10) for i in nodes}
budget = 5
selected_stations = optimize_station_locations(nodes, demand_intensity, budget, max_distance, candidate_stations)
print(f"Selected Stations: {selected_stations}")

# 生成公交路线
graph = nx.random_geometric_graph(100, 0.125)
routes = generate_routes(graph, selected_stations)
print(f"Generated Routes: {routes}")

# 调整频率与排队论
for station in selected_stations:
    demand = np.random.randint(50, 100)
    capacity = 40
    frequency, total_cost = optimize_frequency(demand, capacity)
    print(f"Station {station}: Frequency: {frequency}, Cost: {total_cost}")
