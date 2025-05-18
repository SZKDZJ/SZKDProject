import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import fowlkes_mallows_score, silhouette_score, calinski_harabasz_score, classification_report, \
    mean_squared_error, \
    median_absolute_error, explained_variance_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import SVC

# 读取wine数据集和wine_quality数据集
wine = pd.read_csv('wine.csv', sep=',')
wine_quality = pd.read_csv('winequality.csv', sep=';')

# 数据集的数据和标签拆分
wine_data=wine.iloc[:,1:].values
wine_target=wine['Class'].values
wine_feature_names=wine.columns[1:]

wine_quality_data=wine_quality.iloc[:,:11].values
wine_quality_target=wine_quality['quality'].values
wine_quality_feature_names=wine_quality.columns[:11]

# 将wine_quality数据集划分为训练集和测试集
wine_quality_data_train, wine_quality_data_test, wine_quality_target_train, wine_quality_target_test = (
    train_test_split(wine_quality_data,wine_quality_target,test_size=0.2,random_state=42))
wine_data_train,wine_data_test,wine_target_train,wine_target_test =(
    train_test_split(wine_data,wine_target,test_size=0.2,random_state=42))

# 标准差标准化wine数据集和wine_quality数据集
Scaler = StandardScaler().fit(wine_quality_data_train)
wine_quality_data_trainScaler = Scaler.transform(wine_quality_data_train)
wine_quality_data_testScaler = Scaler.transform(wine_quality_data_test)

Scaler = StandardScaler().fit(wine_data_train)
wine_data_trainScaler = Scaler.transform(wine_data_train)
wine_data_testScaler = Scaler.transform(wine_data_test)
wine_data_Scaler = Scaler.transform(wine_data)

# 对wine数据集和wine_quality数据集进行PCA降维
pca_model = PCA(n_components='mle').fit(wine_quality_data_trainScaler)
wine_quality_data_trainPca = pca_model.transform(wine_quality_data_trainScaler)
wine_quality_data_testPca = pca_model.transform(wine_quality_data_testScaler)
print('wine_quality数据在PCA降维前训练集数据的形状为：',wine_quality_data_trainScaler.shape)
print('wine_quality数据在PCA降维后训练集数据的形状为：',wine_quality_data_trainPca.shape)
print('wine_quality数据在PCA降维前测试集数据的形状为：',wine_quality_data_testScaler.shape)
print('wine_quality数据在PCA降维后测试集数据的形状为：',wine_quality_data_testPca.shape)

pca_model = PCA(n_components='mle').fit(wine_data_trainScaler)
wine_data_trainPca = pca_model.transform(wine_data_trainScaler)
wine_data_testPca = pca_model.transform(wine_data_testScaler)
wine_dataPca = pca_model.transform(wine_data_Scaler)
print('wine数据在PCA降维前训练集数据的形状为：',wine_data_trainScaler.shape)
print('wine数据在PCA降维后训练集数据的形状为：',wine_data_trainPca.shape)
print('wine数据在PCA降维前测试集数据的形状为：',wine_data_testScaler.shape)
print('wine数据在PCA降维后测试集数据的形状为：',wine_data_testPca.shape)
print('wine数据在PCA降维前总数据集数据的形状为：',wine_dataPca.shape)
print('wine数据在PCA降维后总数据集数据的形状为：',wine_dataPca.shape)

# 构建聚类数目为3的K-Means模型
kmeans = KMeans(n_clusters=3,random_state=123).fit(wine_dataPca)
# 计算FMI
FMI_score = fowlkes_mallows_score(wine_target, kmeans.labels_)
print("对比真实标签和聚类标签所得到的Fowlkes-Mallows指数 (FMI):", FMI_score)

# 初始化存储FMI和使用FMI评价法评价K-Means聚类模型的最优聚类数目
best_fmi = 0
best_fmi_score = 0.0
fmiScore = []
# 初始化列表存储轮廓系数
silhouetteScore = []

for i in range(2,11):

    # 构建并训练模型
    kmeans = KMeans(n_clusters = i,random_state=123).fit(wine_dataPca)

    # 在聚类数目为2-10类时，使用FMI评价法评价K-Means聚类模型，确定最优聚类数目
    fmi_score = fowlkes_mallows_score(wine_target, kmeans.labels_)
    fmiScore.append(fmi_score)
    print('wine数据聚%d类FMI评价分值为：%f' %(i,fmi_score))
    if fmi_score > best_fmi_score:
        best_fmi_score = fmi_score
        best_fmi = i

    # 计算轮廓系数
    sil_score = silhouette_score(wine_dataPca, kmeans.labels_)
    silhouetteScore.append(sil_score)

#使用FMI评价法评价K-Means聚类模型的最优聚类数目
print('使用FMI评价法评价K-Means聚类模型的最优聚类数目为：%d 类'%best_fmi)

# 根据模型的FMI，绘制FMI折线图，确定最优聚类数目
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(10,6))
plt.plot(range(2,11), fmiScore, marker='o',linewidth=1.5, linestyle="-")
plt.xlabel('聚类数目')
plt.ylabel('FMI评价分值')
plt.title('不同聚类数目的FMI评价分值')
plt.savefig('不同聚类数目的FMI评价分值.png')
plt.show()

# 根据模型的轮廓系数，绘制轮廓系数折线图，确定最优聚类数目
plt.figure(figsize=(10,6))
plt.plot(range(2,11), silhouetteScore, marker='o',linewidth=1.5, linestyle="-")
plt.xlabel('聚类数目')
plt.ylabel('轮廓系数')
plt.title('不同聚类数目的轮廓系数')
plt.savefig('不同聚类数目的轮廓系数.png')
plt.show()

# 初始化列表存储Calinski-Harabasz指数
best_ch=0
best_ch_score=0.0
chScore=[]
for i in range(2, 11):
    # 构建并训练模型
    kmeans = KMeans(n_clusters=i, random_state=123).fit(wine_dataPca)
    # 计算Calinski-Harabasz指数
    ch_score = calinski_harabasz_score(wine_dataPca, kmeans.labels_)
    chScore.append(ch_score)
    print('wine数据聚%d类Calinski-Harabasz指数为：%f' % (i, ch_score))
    if ch_score > best_ch_score:
        best_ch_score = ch_score
        best_ch = i

#使用Calinski-Harabasz指数评价K-Means聚类模型的最优聚类数目
print('使用Calinski-Harabasz指数评价K-Means聚类模型的最优聚类数目为：%d 类'%best_ch)

# 根据模型的Calinski-Harabasz指数，绘制Calinski-Harabasz指数折线图，确定最优聚类数目
plt.figure(figsize=(10,6))
plt.plot(range(2,11), chScore, marker='o',linewidth=1.5, linestyle="-")
plt.xlabel('聚类数目')
plt.ylabel('Calinski-Harabasz指数')
plt.title('不同聚类数目的Calinski-Harabasz指数')
plt.savefig('不同聚类数目的Calinski-Harabasz指数.png')
plt.show()

# 使用离差标准化方法标准化wine数据集
mScaler = MinMaxScaler().fit(wine_data_train)
wine_data_train_mScaled = mScaler.transform(wine_data_train)
wine_data_test_mScaled = mScaler.transform(wine_data_test)

# 构建SVM模型
svm_model = SVC(random_state=123)
svm_model.fit(wine_data_train_mScaled, wine_target_train)

# 预测测试集结果
wine_target_pred = svm_model.predict(wine_data_test_mScaled)
print('预测结果为：\n', wine_target_pred)

# 求出预测和真实一样的数目
true = np.sum(wine_target_pred == wine_target_test )
print('预测对的结果数目为：', true)
print('预测错的的结果数目为：', wine_target_test.shape[0]-true)
print('预测结果准确率为：', true/wine_target_test.shape[0])

# 打印分类报告，评价分类模型性能
print('使用SVM预测wine数据的分类报告为：\n', classification_report(wine_target_test, wine_target_pred))

# 根据 wine_quality 数据集处理的结果，构建线性回归模型、梯度提升回归模型
# 构建线性回归模型
lin_reg = LinearRegression()
lin_reg.fit(wine_quality_data_trainPca, wine_quality_target_train)
wine_quality_pred_lin = lin_reg.predict(wine_quality_data_testPca)

# 可视化
fig = plt.figure(figsize=(15,6)) # 设定空白画布，并制定大小
plt.plot(range(wine_quality_target_test.shape[0]),wine_quality_target_test,color="dodgerblue", linewidth=1.5, linestyle="-")
plt.plot(range(wine_quality_target_test.shape[0]),wine_quality_pred_lin,color="tomato", linewidth=1.5, linestyle="-.")
plt.legend(['真实值','预测值'])
plt.savefig('线性回归聚类结果.png')
plt.show()

# 构建梯度提升回归模型
gbr = GradientBoostingRegressor(random_state=123)
gbr.fit(wine_quality_data_trainPca, wine_quality_target_train)
wine_quality_pred_gbr = gbr.predict(wine_quality_data_testPca)

# 可视化
fig = plt.figure(figsize=(15,6)) # 设定空白画布，并制定大小
plt.plot(range(wine_quality_target_test.shape[0]),wine_quality_target_test,color="dodgerblue", linewidth=1.5, linestyle="-")
plt.plot(range(wine_quality_target_test.shape[0]),wine_quality_pred_gbr,color="tomato", linewidth=1.5, linestyle="-.")
plt.legend(['真实值','预测值'])
plt.savefig('梯度提升回归聚类结果.png')
plt.show()


# 结合真实评分和预测评分，计算均方误差，中值绝对误差，可解释方差值
for model_name, pred in zip(["线性回归", "梯度提升回归"], [wine_quality_pred_lin, wine_quality_pred_gbr]):
    mse = mean_squared_error(wine_quality_target_test, pred)
    mae = median_absolute_error(wine_quality_target_test, pred)
    evs = explained_variance_score(wine_quality_target_test, pred)

    print(f"{model_name} - 均方误差: {mse:.2f}, 中值绝对误差: {mae:.2f}, 可解释方差: {evs:.2f}")