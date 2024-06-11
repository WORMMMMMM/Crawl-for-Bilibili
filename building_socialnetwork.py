import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 设置matplotlib字体
font = FontProperties(fname=r"C:\Windows\Fonts\HP Simplified Hans.ttc", size=14)  # 指定字体路径和大小

# 读取CSV文件
df = pd.read_csv("social_network.csv")

# 创建有向图
G = nx.DiGraph()

# 根据CSV文件中的sourcename和name列添加边
for index, row in df.iterrows():
    G.add_edge(row['SourceName'], row['NAME'])

# 定义特定名称的节点列表
special_nodes = ['刘守元', '超级草根']  # 替换为你的特定节点名称

# 定义节点颜色
node_colors = ['red' if node in special_nodes else 'skyblue' for node in G.nodes()]

# 可视化图，使用定义的节点颜色
nx.draw(G, with_labels=False, arrowstyle='->', node_color=node_colors, node_size=100)
plt.show()