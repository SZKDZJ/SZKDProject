import numpy as np
import pandas as pd
from scipy.interpolate import lagrange, PchipInterpolator
import matplotlib.pyplot as plt

# 导入 missing_data.xls
data = pd.read_excel('missing_data.xls', header=None)
print("原始数据：")
print(data)

# 查询缺失值所在位置
print("缺失值所在位置：")
print(data.isnull().stack()[data.isnull().stack()])

# 定义拉格朗日插值函数
def lagrange_interpolate(series):
    series = series.copy()
    for i in range(len(series)):
        if pd.isnull(series[i]):
            # 获取非空值的索引和值
            valid_index = series[series.notnull()].index
            valid_values = series[series.notnull()].values
            if len(valid_values) > 1:  # 确保有足够的数据进行插值
                # 使用拉格朗日插值计算缺失值
                series[i] = lagrange(valid_index, valid_values)(i)
            else:
                print(f"插值失败：缺少足够的数据在索引 {i}")
    return series

# 用户A：提取第一列数据为 Pandas Series
data_1 = data.iloc[:, 0]
data_1_lagrange = lagrange_interpolate(data_1)
# 用户B：提取第二列数据为 Pandas Series
data_2 = data.iloc[:, 1]
data_2_lagrange = lagrange_interpolate(data_2)
# 用户C：提取第三列数据为 Pandas Series
data_3 = data.iloc[:, 2]
data_3_lagrange = lagrange_interpolate(data_3)

print("插值前：\n",data)
print("拉格朗日插值后：\n",pd.concat([data_1_lagrange, data_2_lagrange, data_3_lagrange], axis=1))

# 检查是否存在缺失值
print("是否存在缺失值：", pd.concat([data_1_lagrange, data_2_lagrange, data_3_lagrange]).isnull().values.any())

# 验证插值效果
#拉格朗日插值方法在数据间距较大时，特别是边界数据或缺失值较多的情况下，容易产生数值爆炸或异常结果。这种情况是拉格朗日插值的一个已知缺陷，主要原因如下：
#1. **多项式阶数过高**：拉格朗日插值在缺失值位置插入的是一个高阶多项式，数据量越多，插值的多项式阶数越高，容易产生“龙格现象”（Runge's phenomenon），
#   即插值在边界或数据间隙较大时产生大幅波动，导致异常值。
#2. **边界效应**：在插值位置靠近数据的边界处（如数据的开头和结尾）进行拉格朗日插值时，插值的精度通常会降低，因为边界数据缺少足够的邻近点，导致插值不准确。
#3. **连续缺失值**：当数据中连续的缺失值较多时，拉格朗日插值会在这些位置拟合一个过于陡峭的多项式，导致插值结果过大或过小。

# 绘制原始数据和插值后的数据
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
p1 = plt.figure(figsize=(12, 20))

ax1 = p1.add_subplot(3, 1, 1)
plt.plot(data_1, 'o-', label='原始数据A', color='blue')
plt.plot(data_1_lagrange, 'x-', label='拉格朗日插值A', color='orange')
plt.xlabel("数据索引")
plt.ylabel("数据值")
plt.legend()
plt.title("用户A拉格朗日插值效果检验")

ax2 = p1.add_subplot(3, 1, 2)
plt.plot(data_2, 'o-', label='原始数据B', color='dodgerblue')
plt.plot(data_2_lagrange, 'x-', label='拉格朗日插值B', color='tomato')
plt.xlabel("数据索引")
plt.ylabel("数据值")
plt.legend()
plt.title("用户B拉格朗日插值效果检验")

ax3 = p1.add_subplot(3, 1, 3)
plt.plot(data_3, 'o-', label='原始数据C', color='firebrick')
plt.plot(data_3_lagrange, 'x-', label='拉格朗日插值C', color='lightblue')
plt.title("用户C拉格朗日插值效果检验")
plt.xlabel("数据索引")
plt.ylabel("数据值")
plt.legend()
plt.savefig('拉格朗日插值效果检验.png')
plt.show()

# 定义拉格朗日局部插值函数
def lagrange_interpolate_local(series, window=3):

    series = series.copy()  # 防止原始数据被修改
    interpolated_indices = []  # 记录插值的位置索引
    for i in range(len(series)):
        if pd.isnull(series[i]):  # 如果当前值是缺失值
            # 确定窗口范围，避免超出边界
            start = max(0, i - window)
            end = min(len(series), i + window + 1)

            # 获取窗口内的有效数据
            local_series = series[start:end]
            valid_index = local_series[local_series.notnull()].index
            valid_values = local_series[local_series.notnull()].values

            # 如果窗口内有足够数据点，进行插值
            if len(valid_values) > 1:
                series[i] = lagrange(valid_index, valid_values)(i)
                interpolated_indices.append(i)  # 记录插值位置
            else:
                print(f"插值失败：窗口范围内数据不足，索引 {i}")

    return series, interpolated_indices

# 方法1：使用线性插值
data_1_linear = data_1.interpolate(method='linear')
data_2_linear = data_2.interpolate(method='linear')
data_3_linear = data_3.interpolate(method='linear')

# 方法2：使用样条插值（pchip 更适合有界值）
data_1_spline = data_1.interpolate(method='pchip', order=3)
data_2_spline = data_2.interpolate(method='pchip', order=3)
data_3_spline = data_3.interpolate(method='pchip', order=3)

# 方法3：拉格朗日局部插值
data_1_lagrange_local, indicates_1 = lagrange_interpolate_local(data_1)
data_2_lagrange_local, indicates_2 = lagrange_interpolate_local(data_2)
data_3_lagrange_local, indicates_3 = lagrange_interpolate_local(data_3)

print("线性插值后：\n",pd.concat([data_1_linear, data_2_linear, data_3_linear], axis=1))
print("三次样条插值后：\n",pd.concat([data_1_spline, data_2_spline, data_3_spline], axis=1))
print("拉格朗日局部插值后：\n",pd.concat([data_1_lagrange_local, data_2_lagrange_local, data_3_lagrange_local], axis=1))

# 定义生成平滑曲线的函数
def generate_smooth_curve(x, y, resolution=100):

    interpolator = PchipInterpolator(x, y)  # 使用 Pchip 样条插值
    x_smooth = np.linspace(min(x), max(x), resolution)  # 高分辨率 x 轴
    y_smooth = interpolator(x_smooth)  # 平滑的 y 数据
    return x_smooth, y_smooth

datasets = [data_1, data_2, data_3]
names = ["用户A", "用户B", "用户C"]

for i, data in enumerate(datasets):
    data_linear = data.interpolate(method='linear')
    data_spline = data.interpolate(method='pchip', order=3)
    data_lagrange_local, lagrange_indices = lagrange_interpolate_local(data)

    # 绘图
    plt.figure(figsize=(12, 8))

    # 原始数据
    x_original = np.arange(len(data))
    plt.plot(x_original, data, 'o', label=f'原始数据 {names[i]}', color='blue')

    # 拉格朗日局部插值平滑曲线
    x_smooth, y_smooth_lagrange = generate_smooth_curve(
        x_original[~pd.isnull(data_lagrange_local)],
        data_lagrange_local.dropna(),
        resolution=200
    )
    plt.plot(x_smooth, y_smooth_lagrange, '-', label=f'拉格朗日局部插值 {names[i]} (平滑)', color='orange')
    plt.scatter(
        lagrange_indices,
        data_lagrange_local[lagrange_indices],
        color='orange', marker='x', label=f'拉格朗日插值点 {names[i]}'
    )

    # 线性插值平滑曲线
    x_smooth, y_smooth_linear = generate_smooth_curve(
        x_original[~pd.isnull(data_linear)],
        data_linear.dropna(),
        resolution=200
    )
    plt.plot(x_smooth, y_smooth_linear, '--', label=f'线性插值 {names[i]} (平滑)', color='dodgerblue')
    plt.scatter(
        data_linear.index[data.isnull()],
        data_linear[data.isnull()],
        color='dodgerblue', marker='x', label=f'线性插值点 {names[i]}'
    )

    # 三次样条插值平滑曲线
    x_smooth, y_smooth_spline = generate_smooth_curve(
        x_original[~pd.isnull(data_spline)],
        data_spline.dropna(),
        resolution=200
    )
    plt.plot(x_smooth, y_smooth_spline, '-.', label=f'三次样条插值 {names[i]} (平滑)', color='tomato')
    plt.scatter(
        data_spline.index[data.isnull()],
        data_spline[data.isnull()],
        color='tomato', marker='x', label=f'三次样条插值点 {names[i]}'
    )

    plt.xlabel("数据索引")
    plt.ylabel("数据值")
    plt.title(f"{names[i]} 的不同插值效果对比（平滑曲线）")
    plt.legend()
    plt.grid()
    plt.savefig(f"{names[i]}的插值效果对比.png")
    plt.show()

# 读取 ele_loss.csv 和 alarm.csv
ele_loss = pd.read_csv('ele_loss.csv')
alarm = pd.read_csv('alarm.csv',encoding='gb18030')

# 查看两表的形状
print("ele_loss 形状：", ele_loss.shape)
print("alarm 形状：", alarm.shape)

# 以ID和date两个键值作为主键进行内连接
merged_data = pd.merge(ele_loss, alarm, on=['ID', 'date'], how='inner')
print('合并后数据形状为:',merged_data.shape)
print("合并后的数据：")
print(merged_data)

# 读取 model.csv 数据，定义标准差标准化函数，对3列数据标准化
model_data = pd.read_excel('model.xls')

# 定义标准差标准化函数
def standardize(series):
    return (series - series.mean()) / series.std()

#所有列进行标准化
for col in model_data.columns:
    model_data[col]=standardize(model_data[col])

print("标准化后的数据：")
print(model_data)