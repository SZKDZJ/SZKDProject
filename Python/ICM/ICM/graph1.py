import pandas as pd
import networkx as nx
from shapely import wkt
import geopandas as gpd
import numpy as np
import heapq
from geopy.distance import geodesic
from collections import defaultdict
from functools import lru_cache
import matplotlib.pyplot as plt

# ====================== 参数配置 ======================#
BRIDGE_REF = "I 695"  # 需要移除的桥梁标识
AADT_FILE = "MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.csv"
ALPHA = 0.15  # BPR函数参数
BETA = 4


# ====================== 数据加载模块 ======================#
class TrafficDataLoader:
    @staticmethod
    def load_nodes(path):
        """加载节点数据"""
        nodes = pd.read_excel(path)
        nodes['geometry'] = nodes['geometry'].apply(wkt.loads)
        return gpd.GeoDataFrame(nodes, geometry='geometry').set_crs("EPSG:4326")

    @staticmethod
    def load_edges(path):
        """加载边数据"""
        edges = pd.read_excel(path)
        edges['geometry'] = edges['geometry'].apply(wkt.loads)
        return gpd.GeoDataFrame(edges, geometry='geometry').set_crs("EPSG:4326")

    @staticmethod
    def load_aadt(path):
        """加载流量数据"""
        try:
            # 1. 加载数据
            df = pd.read_csv(path, encoding='utf-8-sig')
            print("原始列名:", df.columns.tolist())

            # 2. 标准化列名
            df.columns = (
                df.columns
                .str.strip()  # 去除前后空格
                .str.lower()  # 转为小写
                .str.replace(r'[^\w]', '_', regex=True)  # 替换特殊字符为下划线
                .str.replace(r'_+', '_', regex=True)  # 合并连续下划线
            )
            print("标准化后列名:", df.columns.tolist())

            # 3. 动态列名映射
            column_mapping = {
                'u': next(col for col in df.columns if 'node_start' in col),
                'v': next(col for col in df.columns if 'node_s_end' in col),
                'aadt': next(col for col in df.columns if 'aadt_current' in col),
                'lanes': next(col for col in df.columns if 'number_of_lanes' in col)
            }
            print("使用的列映射:", column_mapping)

            df_clean = df.rename(columns=column_mapping)

            # 4. 清洗节点ID
            def clean_node(value):
                try:
                    return int(''.join(filter(str.isdigit, str(value))))
                except:
                    return 0

            df_clean['u'] = df_clean['u'].apply(clean_node)
            df_clean['v'] = (
                df_clean['v']
                .astype(str)
                .str.split(';')
                .explode()
                .apply(clean_node)
            )

            # 5. 过滤无效数据
            df_clean = df_clean.query('u > 0 and v > 0')

            return df_clean[['u', 'v', 'aadt', 'lanes']].reset_index(drop=True)

        except Exception as e:
            print(f"错误详情: {str(e)}")
            available_cols = "\n".join(df.columns) if 'df' in locals() else "无数据"
            print(f"可用列名:\n{available_cols}")
            raise
# ====================== 图构建模块 ======================#
class EnhancedTrafficNetwork:
    def __init__(self):
        self.G = nx.DiGraph()
        self.edge_mapping = {}  # 存储(u,v)到属性的映射

    def build_network(self, nodes_gdf, edges_gdf, aadt_df):
        """构建带流量属性的交通网络"""
        # 添加节点
        for _, row in nodes_gdf.iterrows():
            self.G.add_node(row['osmid'],
                            pos=(row['geometry'].x, row['geometry'].y),
                            **row.drop(['geometry', 'osmid']).to_dict())

        # 添加边并合并流量数据
        edges_merged = edges_gdf.merge(
            aadt_df,
            on=['u', 'v'],
            how='left',
            suffixes=('', '_aadt')
        )

        for _, row in edges_merged.iterrows():
            # 基础属性
            attrs = {
                'length': row['length'],
                'maxspeed': self._parse_speed(row['maxspeed']),
                'lanes': row.get('lanes', 1),
                'bridge': row.get('bridge', 'no'),
                'ref': row.get('ref', '')
            }

            # 流量相关属性
            traffic_attrs = {
                'AADT': row.get('AADT', 0),
                'AADT_car': row.get('AADT Car', 0),
                'AADT_truck': row.get('AADT Light Truck', 0),
                'AADT_bus': row.get('AADT Bus', 0)
            }

            self.G.add_edge(row['u'], row['v'], **{**attrs, **traffic_attrs})
            self.edge_mapping[(row['u'], row['v'])] = traffic_attrs

    def _parse_speed(self, speed_str):
        """解析速度字符串（支持多种格式）"""
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
        """移除指定桥梁边"""
        edges_to_remove = [
            (u, v) for u, v, attrs in self.G.edges(data=True)
            if attrs.get('ref') == BRIDGE_REF and attrs.get('bridge') == 'yes'
        ]
        self.G.remove_edges_from(edges_to_remove)
        return edges_to_remove


# ====================== 连通性分析模块 ======================#
class ConnectivityAnalyzer:
    @staticmethod
    def check_connectivity(graph):
        """增强型连通性检查"""
        # 检查弱连通性
        is_weak = nx.is_weakly_connected(graph)

        # 检查强连通性
        is_strong = nx.is_strongly_connected(graph)

        # 检查连通组件数量
        weak_components = nx.number_weakly_connected_components(graph)
        strong_components = nx.number_strongly_connected_components(graph)

        return {
            'weak_connectivity': is_weak,
            'strong_connectivity': is_strong,
            'weak_components': weak_components,
            'strong_components': strong_components
        }


# ====================== 路径规划模块 ======================#
class AdvancedPathFinder:
    def __init__(self, graph):
        self.G = graph
        self.path_cache = {}

    @lru_cache(maxsize=None)
    def _heuristic(self, n1, n2):
        """动态启发式函数（考虑实时交通）"""
        p1 = self.G.nodes[n1]['pos']
        p2 = self.G.nodes[n2]['pos']
        return geodesic(p1, p2).kilometers * 0.8  # 加入修正因子

    def a_star_search(self, start, end, time_weight=1.0, cost_weight=0.0):
        """
        多目标A*算法
        :param time_weight: 时间权重 (0.0-1.0)
        :param cost_weight: 成本权重 (0.0-1.0)
        """
        open_heap = []
        heapq.heappush(open_heap, (0, start))
        g_score = defaultdict(lambda: float('inf'))
        g_score[start] = 0
        came_from = {}

        while open_heap:
            current_f, current = heapq.heappop(open_heap)

            if current == end:
                return self._reconstruct_path(came_from, end), g_score[end]

            for neighbor in self.G.neighbors(current):
                edge_data = self.G[current][neighbor]

                # 计算综合代价
                time_cost = edge_data['length'] / (edge_data['maxspeed'] * 1000)
                economic_cost = edge_data.get('toll', 0) * 0.1  # 假设有过路费属性

                tentative_g = g_score[current] + \
                              time_weight * time_cost + \
                              cost_weight * economic_cost

                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self._heuristic(neighbor, end)
                    heapq.heappush(open_heap, (f_score, neighbor))

        return None, float('inf')

    def _reconstruct_path(self, came_from, end):
        """可视化友好的路径重建"""
        path = [end]
        while end in came_from:
            end = came_from[end]
            path.append(end)
        return {
            'nodes': path[::-1],
            'segments': list(zip(path[:-1], path[1:]))
        }

    def precompute_critical_paths(self, od_pairs):
        """预计算关键OD对路径"""
        for origin, destination in od_pairs:
            if origin in self.G and destination in self.G:
                self.path_cache[(origin, destination)] = self.a_star_search(origin, destination)


# ====================== 流量分析模块 ======================#
class TrafficFlowAnalyzer:
    def __init__(self, graph):
        self.G = graph
        self.congestion_threshold = 0.85  # 拥堵阈值

    def calculate_capacity(self, lanes):
        """计算路段通行能力"""
        return 1800 * lanes  # 辆/小时

    def incremental_assignment(self, od_matrix, iterations=4):
        """改进的增量分配法"""
        edge_flows = defaultdict(float)
        total_flow = od_matrix.sum().sum()

        # 分阶段分配（40%-30%-20%-10%）
        for i, frac in enumerate([0.4, 0.3, 0.2, 0.1]):
            print(f"正在分配第{i + 1}阶段流量 ({frac * 100}%)")

            # 分配流量
            flow_part = total_flow * frac
            for (origin, dest), demand in od_matrix.items():
                path_result = self.find_optimal_path(origin, dest)
                if not path_result:
                    continue

                # 按比例分配流量到各路段
                for u, v in path_result['segments']:
                    capacity = self.calculate_capacity(self.G[u][v]['lanes'])
                    allocated_flow = min(demand * frac, capacity * 0.8)  # 防止过载
                    edge_flows[(u, v)] += allocated_flow

            # 更新路段属性
            self.update_edge_properties(edge_flows)

        return edge_flows

    def find_optimal_path(self, origin, dest):
        """动态路径规划（可扩展实时交通）"""
        return self.G.path_finder.a_star_search(origin, dest)

    def update_edge_properties(self, edge_flows):
        """更新路段通行时间"""
        for (u, v), flow in edge_flows.items():
            edge = self.G[u][v]
            capacity = self.calculate_capacity(edge['lanes'])

            # BPR函数计算拥堵时间
            t_free = edge['length'] / (edge['maxspeed'] * 1000)
            edge['congestion_time'] = t_free * (1 + ALPHA * (flow / capacity) ** BETA)

            # 计算负荷度
            edge['v_c_ratio'] = flow / capacity

    def identify_congestions(self):
        """识别拥堵路段"""
        congestions = []
        for u, v, data in self.G.edges(data=True):
            if data.get('v_c_ratio', 0) > self.congestion_threshold:
                congestions.append({
                    'from': u,
                    'to': v,
                    'v_c_ratio': data['v_c_ratio'],
                    'congestion_time': data['congestion_time']
                })
        return congestions


# ====================== 主程序 ======================#
if __name__ == "__main__":
    # 1. 加载数据
    print("正在加载数据...")
    nodes = TrafficDataLoader.load_nodes("node_allNew.xlsx")
    edges = TrafficDataLoader.load_edges("edges_allNew.xlsx")
    aadt_data = TrafficDataLoader.load_aadt("/Users/eureka/Desktop/2025_Problem_D_Data/MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.csv")

    # 2. 构建交通网络
    print("构建交通网络中...")
    traffic_net = EnhancedTrafficNetwork()
    traffic_net.build_network(nodes, edges, aadt_data)

    # 3. 连通性分析
    print("\n网络连通性分析:")
    conn_result = ConnectivityAnalyzer.check_connectivity(traffic_net.G)
    print(f"弱连通性: {conn_result['weak_connectivity']}")
    print(f"强连通性: {conn_result['strong_connectivity']}")
    print(f"弱连通组件数: {conn_result['weak_components']}")
    print(f"强连通组件数: {conn_result['strong_components']}")

    # 4. 移除桥梁边
    removed_edges = traffic_net.remove_bridge_edges()
    print(f"\n移除了 {len(removed_edges)} 条桥梁边")

    # 5. 初始化路径规划器
    path_finder = AdvancedPathFinder(traffic_net.G)
    traffic_net.G.path_finder = path_finder

    # 6. 流量分配
    print("\n开始流量分配...")
    analyzer = TrafficFlowAnalyzer(traffic_net.G)

    # 生成示例OD矩阵（实际应用需替换为真实数据）
    sample_od = pd.DataFrame(
        np.random.randint(100, 500, (len(traffic_net.G.nodes), len(traffic_net.G.nodes))),
        index=traffic_net.G.nodes,
        columns=traffic_net.G.nodes
    )
     # 调用改进的增量分配方法，传入完整的OD矩阵
    edge_flows = analyzer.incremental_assignment(sample_od)

    # 7. 拥堵分析
    print("\n拥堵路段分析:")
    congestions = analyzer.identify_congestions()
    print(f"发现 {len(congestions)} 条拥堵路段")
    if congestions:
        print("前3条严重拥堵路段:")
        for c in sorted(congestions, key=lambda x: x['v_c_ratio'], reverse=True)[:3]:
            print(f"路段 {c['from']}->{c['to']}: 负荷度={c['v_c_ratio']:.2f}, 拥堵时间={c['congestion_time']:.2f}小时")

    # 8. 可视化（示例）
    pos = nx.get_node_attributes(traffic_net.G, 'pos')
    nx.draw(traffic_net.G, pos, with_labels=True, node_size=200, font_size=8)
    nx.draw_networkx_edges(
        traffic_net.G, pos,
        edgelist=[(c['from'], c['to']) for c in congestions],
        edge_color='r',
        width=[min(3, 2 + c['v_c_ratio'] * 5) for c in congestions]
    )
    plt.title("交通网络拥堵分析")
    plt.savefig("congestion_analysis.png", dpi=300)
    print("\n可视化结果已保存至 congestion_analysis.png")
