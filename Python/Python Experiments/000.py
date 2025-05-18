import matplotlib.pyplot as plt
from matplotlib import rcParams

# 设置中文字体，使用系统字体，例如 'PingFang SC'
rcParams['font.family'] = 'STXinwei'

# 绘图示例
plt.text(0.5, 0.5, '你好，世界！', fontsize=15, ha='center')
plt.text(0.5, 0.5, 'hello！！', fontsize=15, ha='center')
plt.show()