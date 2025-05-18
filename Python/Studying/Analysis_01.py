import matplotlib.pyplot as plt
import networkx as nx

# 创建技能树图
G = nx.DiGraph()

# 添加根节点和主要分支
G.add_edges_from([
    ("人工智能算法工程师", "数学与理论基础"),
    ("人工智能算法工程师", "算法与模型"),
    ("人工智能算法工程师", "编程与实现"),
    ("人工智能算法工程师", "数据处理与工程化"),
    ("人工智能算法工程师", "系统与工具"),
    ("人工智能算法工程师", "大数据与分布式计算"),
    ("人工智能算法工程师", "软技能")
])

# 添加子技能
# 数学与理论基础
G.add_edges_from([
    ("数学与理论基础", "线性代数"),
    ("数学与理论基础", "概率与统计"),
    ("数学与理论基础", "微积分"),
    ("数学与理论基础", "优化理论"),
    ("数学与理论基础", "信息论"),
])

# 算法与模型
G.add_edges_from([
    ("算法与模型", "机器学习"),
    ("算法与模型", "深度学习"),
    ("算法与模型", "推荐系统"),
    ("算法与模型", "图神经网络"),
])
G.add_edges_from([
    ("机器学习", "监督学习"),
    ("机器学习", "无监督学习"),
    ("机器学习", "强化学习"),
])
G.add_edges_from([
    ("深度学习", "CNN"),
    ("深度学习", "RNN"),
    ("深度学习", "Transformer"),
])

# 编程与实现
G.add_edges_from([
    ("编程与实现", "Python"),
    ("编程与实现", "C++"),
    ("编程与实现", "TensorFlow"),
    ("编程与实现", "PyTorch"),
])

# 绘图
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42, k=0.5)  # 调整布局参数

nx.draw_networkx_nodes(G, pos, node_size=3000, node_color="lightblue")
nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=15, edge_color="gray")
nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

plt.title("人工智能算法工程师技能树", fontsize=14)
plt.axis("off")
plt.show()