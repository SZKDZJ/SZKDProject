import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 加载数据
data = np.load('数据分析1数据-populations.npz', allow_pickle=True)

# 设置中文字体和负号显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 使用 Arial Unicode MS 或其他支持中文的字体
plt.rcParams['axes.unicode_minus'] = False

# 提取特征名称和数据
name = data['feature_names']
values = data['data']
values = np.flip(values, axis=0)
print(values)
print(name)

# 去除空值
values = np.delete(values, [0,1], axis=0)

# 使用列表推导式清理年份数据
values[:, 0] = [int(str(year).replace('年', '').strip()) for year in values[:, 0]]
print(values)

# 将剩余数据转换为浮点数，并处理缺失值
values = np.array(values, dtype=float)

# 创建散点图绘图窗口
p1 = plt.figure(figsize=(12, 12))

# 子图1
ax1 = p1.add_subplot(2, 1, 1)
# 绘制散点图
plt.scatter(values[:, 0], values[:, 1], marker='o', c='r')
plt.scatter(values[:, 0], values[:, 2], marker='o', c='b')
plt.scatter(values[:, 0], values[:, 3], marker='o', c='g')
# 设置标签和标题
plt.xlabel('年份')
plt.ylabel('人口数量(万人)')
plt.xticks([1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,2008,2009,2010,2011,2012,2013,2014,2015])
plt.title('1996--2015年男女人口数据散点图')
# 添加图例
plt.legend(['年末总人口(万人)', '男性人口(万人)', '女性人口(万人)'])

# 子图2
ax2 = p1.add_subplot(2, 1, 2)
# 绘制散点图
plt.scatter(values[:, 0], values[:, 1], marker='o', c='r')
plt.scatter(values[:, 0], values[:, 4], marker='o', c='y')
plt.scatter(values[:, 0], values[:, 5], marker='o', c='c')
# 设置标签和标题
plt.xlabel('年份')
plt.ylabel('人口数量(万人)')
plt.xticks([1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,2008,2009,2010,2011,2012,2013,2014,2015])
plt.title('1996--2015年城乡人口数据散点图')
# 添加图例
plt.legend(['年末总人口(万人)', '城镇人口(万人)', '乡村人口(万人)'])

# 保存图像
plt.savefig('1996--2015年人口数据散点图.png')
# 显示图表
plt.show()

# 创建柱状图绘图窗口/
p2 = plt.figure(figsize=(12, 12))

# 子图1
ax3 = p2.add_subplot(2, 1, 1)
plt.bar(values[:, 0], values[:, 2],width = 0.5,color='dodgerblue',alpha=0.5,label='男性人口(万人)')
plt.bar(values[:, 0]+0.5, values[:, 3],width = 0.5,color='tomato',alpha=0.5,label='女性人口(万人)')
plt.xlabel('年份')
plt.ylabel('人口数量(万人)')
plt.xticks([1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,2008,2009,2010,2011,2012,2013,2014,2015])
plt.legend()
plt.title('1996--2015年男女人口数据柱状图')

# 子图2
ax4 = p2.add_subplot(2, 1, 2)
plt.bar(values[:, 0], values[:, 4],width = 0.5,color='firebrick',alpha=0.5,label='城镇人口(万人)')
plt.bar(values[:, 0]+0.5, values[:, 5],width = 0.5,color='lightblue',alpha=0.5,label='乡村人口(万人)')
plt.xlabel('年份')
plt.ylabel('人口数量(万人)')
plt.xticks([1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,2008,2009,2010,2011,2012,2013,2014,2015])
plt.legend()
plt.title('1996--2015年城乡人口数据柱状图')

plt.savefig('1996--2015年人口数据柱状图.png')
plt.show()

#创建饼图画布1
p3 = plt.figure(figsize=(12, 8))

# 子图1
ax5 = p3.add_subplot(2, 3, 1)
label1= ['男性人口','女性人口']
color1 = ['wheat','goldenrod']
explode = [0.01,0.01]
plt.pie(values[0,2:4],explode=explode,labels=label1, autopct='%1.1f%%',colors=color1)
plt.legend()
plt.title('1996年男女人口比例饼状图')

# 子图2
ax6 = p3.add_subplot(2, 3, 2)
explode = [0.01,0.01]
plt.pie(values[5,2:4],explode=explode,labels=label1, autopct='%1.1f%%',colors=color1)
plt.legend()
plt.title('2001年男女人口比例饼状图')

# 子图3
ax7 = p3.add_subplot(2, 3, 3)
explode = [0.01,0.01]
plt.pie(values[10,2:4],explode=explode,labels=label1, autopct='%1.1f%%',colors=color1)
plt.legend()
plt.title('2006年男女人口比例饼状图')

# 子图4
ax8 = p3.add_subplot(2, 3, 4)
explode = [0.01,0.01]
plt.pie(values[15,2:4],explode=explode,labels=label1, autopct='%1.1f%%',colors=color1)
plt.legend()
plt.title('2011年男女人口比例饼状图')

# 子图5
ax9 = p3.add_subplot(2, 3, 5)
explode = [0.01,0.01]
plt.pie(values[-1,2:4],explode=explode,labels=label1, autopct='%1.1f%%',colors=color1)
plt.legend()
plt.title('2015年男女人口比例饼状图')

# 调整整个图表的间距和大小
plt.tight_layout()
plt.savefig('1996--2015年男女人口比例饼状图.png')
plt.show()

#创建饼图画布2
p4= plt.figure(figsize=(12,8))

# 子图1
ax10= p4.add_subplot(2, 3, 1)
label2= ['城镇人口','乡村人口']
color2 = ['darkseagreen','powderblue']
plt.pie(values[0,4:6],explode=explode,labels=label2, autopct='%1.1f%%',colors=color2)
plt.legend()
plt.title('1996年城乡人口比例饼状图')

# 子图2
ax11 = p4.add_subplot(2, 3, 2)
explode = [0.01,0.01]
plt.pie(values[5,4:6],explode=explode,labels=label2, autopct='%1.1f%%',colors=color2)
plt.legend()
plt.title('2001年男女人口比例饼状图')

# 子图3
ax12 = p4.add_subplot(2, 3, 3)
explode = [0.01,0.01]
plt.pie(values[10,4:6],explode=explode,labels=label2, autopct='%1.1f%%',colors=color2)
plt.legend()
plt.title('2006年男女人口比例饼状图')

# 子图4
ax13 = p4.add_subplot(2, 3, 4)
explode = [0.01,0.01]
plt.pie(values[15,4:6],explode=explode,labels=label2, autopct='%1.1f%%',colors=color2)
plt.legend()
plt.title('2011年男女人口比例饼状图')

# 子图5
ax14 = p4.add_subplot(2, 3, 5)
plt.pie(values[-1,4:6],explode=explode,labels=label2, autopct='%1.1f%%',colors=color2)
plt.legend()
plt.title('2015年城乡人口比例饼状图')

# 调整整个图表的间距和大小
plt.tight_layout()
plt.savefig('1996--2015年城乡人口比例饼状图.png')
plt.show()

#创建箱线图画布
p5= plt.figure(figsize=(12,12))

plt.boxplot((list(values[:,1]),list(values[:,2]),list(values[:,3]),list(values[:,4]),list(values[:,5])),
                                                     notch=True,tick_labels =
                                                   ['年末总人口','男性人口','女性人口','城镇人口','乡村人口'], meanline=True)
plt.ylabel('人口数量(万人)')
plt.title('1996--2015年人口数据箱线图')

plt.savefig('1996--2015年人口数据箱线图.png')
plt.show()

#创建折线图画布
p6= plt.figure(figsize=(12,12))

plt.plot(values[:, 0], values[:, 1], color='maroon', linestyle='-',linewidth=2)
plt.plot(values[:, 0], values[:, 2], color='steelblue', linestyle='-',linewidth=2)
plt.plot(values[:, 0], values[:, 3], color='lightsteelblue', linestyle='-',linewidth=2)
plt.plot(values[:, 0], values[:, 4], color='darksalmon', linestyle='-',linewidth=2)
plt.plot(values[:, 0], values[:, 5], color='rosybrown', linestyle='-',linewidth=2)
plt.xlabel('年份')
plt.ylabel('人口数量(万人)')
plt.title('1996--2015年人口数据折线图')
plt.grid(which="major", axis='x', color='#DAD8D7', alpha=0.5, zorder=1)
plt.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)
plt.legend(['年末总人口(万人)', '男性人口(万人)', '女性人口(万人)', '城镇人口(万人)', '乡村人口(万人)'])
plt.savefig('1996--2015年人口数据折线图.png')
plt.show()