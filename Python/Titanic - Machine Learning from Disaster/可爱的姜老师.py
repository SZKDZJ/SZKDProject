import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题

#读取数据
data_train = pd.read_csv('train.csv')#读取数据
data_train.head(30)
data_train.info()
data_train.describe()
fig=plt.figure()#画布
fig.set(alpha=0.2)#设定图表颜色alpha参数

plt.subplot2grid((2,3),(0,0))#在一张大图里分列几个小图
data_train.Survived.value_counts().plot(kind='bar') # 柱状图
'''
data_train.Survived：从 data_train DataFrame 中选择名为 Survived 的列
value_counts():计算某列中每个唯一值的出现次数。这会返回一个新的 Series，其中索引是唯一值（例如 0 和 1），值是这些唯一值的计数。
plot(kind='bar')：会将不同的唯一值（0 和 1）作为 x 轴，并将对应的计数作为 y 轴，展示生存和未生存的乘客数量。
'''
plt.title('Survived(1是幸存)')#标题
plt.ylabel('频次')


plt.subplot2grid((2,3),(0, 1))
data_train.Pclass.value_counts().plot (kind="bar")
plt.ylabel( '频次')
plt.title('Distribution of Pclass（舱位等级）')



plt.subplot2grid((2,3),(0,2))
plt.scatter(data_train.Survived, data_train.Age)
plt.ylabel( '年龄 Age')#设定纵坐标名称
plt.grid(visible=True, which='major', axis='y')
# plt.title('Survived by age(1 is yes)')
plt.title('年龄与幸存')
'''
生存状态和年龄的关系：
摄取的每个点在图上的位置使得观察者可以快速了解年龄是否与生存状态有任何统计相关性。
例如：如果大多数年轻乘客（例如 0-20 岁）都生存下来，而年长乘客则大多未生存，图中会显示这种趋势。
'''

plt.subplot2grid((2,3),(1,0),colspan=2)
data_train.Age[data_train.Pclass == 1].plot (kind='kde')
data_train.Age[data_train.Pclass== 2].plot (kind='kde')
data_train.Age[data_train.Pclass== 3].plot (kind='kde')
plt.xlabel('年龄 Age')# plots an axis lable
plt.ylabel('核密度 Desity')
# plt.title( 'Distribution of age')
plt.title( '年龄分布')
plt.legend(('1class','2class','3class'),loc='best')

plt.subplot2grid((2,3),(1,2))
data_train.Embarked.value_counts().plot (kind='bar')
plt.title('登船港口的频数')
plt.xlabel('登船港口')
plt.ylabel('频数')

# 调整子图之间的间距
plt.subplots_adjust(hspace=0.5, wspace=2)  # 调整高度和宽度之间的间距

plt.show()
#2.2.1看看各乘客等级的获救情况
fig =plt.figure()
fig.set(alpha=0.2) #设定图表颜色alpha参数

Survived_0=data_train.Pclass[data_train.Survived == 0].value_counts()
Survived_1=data_train.Pclass[data_train.Survived == 1].value_counts()
df=pd.DataFrame({'No survivd':Survived_0,'Survived':Survived_1})
df.plot (kind='bar', stacked=True)
plt.title('Survived by Pclass')
plt.xlabel('舱位等级 Pclass')
plt.ylabel('频数')
plt.show()
#2.2.2查看各性别的获救情况
fig =plt.figure()#设定图表颜色alpba参数
fig.set(alpha=0.2)

Survived_m= data_train.Survived[data_train.Sex =='male'].value_counts() # 男性的获救情况
Survived_f= data_train.Survived[data_train.Sex == 'female'].value_counts() # 女性的获救情况
df=pd.DataFrame({ 'Male':Survived_m,'Female':Survived_f})
df.plot (kind= 'bar' , stacked=True)
plt.title( 'Survived by Sex')
plt.xlabel('Survived ')
plt.ylabel('频数')
plt.show()

#2.2.3查看各种舱级别情况下各性别的获救情况
fig=plt.figure()
fig.set(alpha=0.65)#设置图像透明度，无所谓
plt.title( 'Survived by sex and Pclass')

ax1=fig.add_subplot(141)
data_train. Survived[data_train.Sex == 'female'][data_train.Pclass != 3].value_counts().sort_index().plot(kind='bar',label="female highclass",color='#FA2479')
ax1.set_xticks([0,1])
ax1.set_xticklabels(['Not S','S'],rotation=0)
ax1.legend(['Female/High class'], loc='best')

ax2=fig.add_subplot(142,sharey=ax1)
data_train.Survived[data_train.Sex=='female'][data_train.Pclass == 3].value_counts(). sort_index(). plot(kind='bar',label= 'female, low class', color='pink')
ax2.set_xticklabels(['Not S','s'],rotation=0)
plt.legend(['Female/Low class'], loc= 'best')

ax3=fig.add_subplot(143,sharey=ax1)
data_train.Survived[data_train.Sex == 'male'][data_train.Pclass != 3].value_counts().sort_index().plot(kind='bar',label='male, high class',color='lightblue')
ax3.set_xticklabels(['Not S','S'],rotation=0)
plt.legend(['Male/High class'], loc='best')

ax4=fig.add_subplot(144,sharey=ax1)
data_train.Survived[data_train.Sex=='male'][data_train.Pclass == 3].value_counts().sort_index().plot(kind='bar',label='male low class' ,color='steelblue')
ax4.set_xticklabels(['Not S','S'],rotation=0)
plt.legend(['Male/Low class'], loc='best')

plt.show()

# 2.2.4 查看各登船港口的获救情况
fig = plt.figure()
fig.set(alpha=0.2)#设定图表颜色alpha参数
Survived_0= data_train.Embarked[data_train.Survived == 0].value_counts()
Survived_1= data_train.Embarked[data_train.Survived == 1].value_counts()
df=pd.DataFrame({'Not Survived':Survived_0,'Survived':Survived_1})
df.plot (kind='bar' , stacked=True)
plt.title( 'Survived by Embarked ')
plt.xlabel( 'Embarked')
plt.ylabel('Counts' )
plt.show()

#2.2.5查看堂兄弟/妹，孩子/父母有几人，对是否获救的影响
gg= data_train.groupby([ 'SibSp','Survived'])
df = pd.DataFrame(gg.count()['PassengerId'])
print(df)

gp = data_train. groupby(['Parch','Survived'])
df = pd. DataFrame(gp.count()['PassengerId'])
print(df)

#2.2.6 tickets cabin的分析
'''
ticket是船票编号，应该是unique的，
和最后的结果没有太大的关系，先不纳入考虑的特征范畴,
cabin只有204个乘客有值，我们先看看它的一个分布:
'''
data_train.Cabin.value_counts()

#2.2.7 查看在有无Cabin信息这个粗粒度上Survived的情况fig=plt.figure()fig.set(alpha=0.2)
Survived_cabin = data_train.Survived[pd.notnull(data_train.Cabin)].value_counts()
Survived_nocabin = data_train.Survived[pd.isnull(data_train.Cabin)].value_counts()
df=pd.DataFrame({'Yes':Survived_cabin, 'No':Survived_nocabin}).transpose()
df.plot(kind= 'bar', stacked=True)
plt.title('Survived by cabin')
plt.xlabel( 'Cabin is yes or no' )
plt.ylabel( 'Counts')
plt.show()

from sklearn.ensemble import RandomForestRegressor

###使用RandomForestClassifier填补缺失的年龄属性
def set_missing_ages(df):
#把已有的数值型特征取出来丢进RandomForestRegressor中
    age_df = df[['Age','Fare','Parch','SibSp','Pclass']]
    #乘客分成已知年龄和未知年龄两部分
    known_age = age_df[age_df.Age.notnull()].values
    unknown_age =age_df[age_df.Age.isnull()].values
    #y即目标年龄
    y=known_age[:,0]
    #X即特征属性值
    X=known_age[:,1:]
    #fit到RandomForestRegressor之中
    rfr =RandomForestRegressor(random_state=0,n_estimators=2000,n_jobs=-1)
    rfr.fit(X, y)
    #用得到的模型进行未知年龄结果预测
    predictedAges =rfr.predict(unknown_age[:,1::])
    #用得到的预测结果填补原缺失数据
    df.loc[(df.Age.isnull()),'Age']=predictedAges
    return df, rfr

#将有Cabin记录的替换成“yes”，将无Cabin记录的替换成“no”
def set_Cabin_type(df):
    df.loc[(df.Cabin.notnull()),'Cabin']="Yes"
    df.loc[(df.Cabin.isnull()),'Cabin']="No"
    return df

data_train,rfr = set_missing_ages(data_train)
data_train = set_Cabin_type(data_train)
data_train.head(10)

dummies_Cabin =pd.get_dummies(data_train['Cabin'],prefix='Cabin')
dummies_Embarked=pd.get_dummies(data_train['Embarked'],prefix='Embarked')
dummies_Sex =pd.get_dummies(data_train['Sex'],prefix='Sex')
dummies_Pclass =pd.get_dummies(data_train['Pclass'],prefix='Pclass')
df=pd.concat([data_train,dummies_Cabin,dummies_Embarked,dummies_Sex,dummies_Pclass],axis=1)
df. drop(['Pclass','Name','Sex','Ticket','Cabin','Embarked'],axis=1,inplace=True)
df.head()

import sklearn.preprocessing as preprocessing
scaler =preprocessing.StandardScaler()

age_scale_param = scaler.fit(df['Age'].values.reshape(-1,1))
df['Age_scaled']= scaler.fit_transform(df['Age'].values.reshape(-1,1),age_scale_param)
fare_scale_param = scaler.fit(df['Fare'].values.reshape(-1,1))
df['Fare_scaled']=scaler.fit_transform(df['Fare'].values.reshape(-1,1),fare_scale_param)
df.head(10)

from sklearn import linear_model
train_df = df.filter(regex= 'Survived|Age_.*|SibSp|Parch|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
print(train_df)
print("X:")
print(train_df[train_df.columns[1:]])
train_np = train_df.values
# print(train_np)
# y即第0列：Survival结果
y=train_np[:,0]
y = y.astype(int)
# X即第1列及以后：特征属性值
X= train_np[:, 1:]
print(X.shape)
print(X)

# fit到LogisticRegression之中
clf = linear_model.LogisticRegression(solver='liblinear',C=1.0, penalty= 'l1',tol=1e-6, max_iter=200)
clf.fit (X,y)

data_test =pd.read_csv("test.csv")
data_test.loc[(data_test.Fare.isnull()),'Fare']=0
#接着我们对test_data做和train_data中一致的特征变换

#首先用同样的RandomForestRegressor模型填上丢失的年龄
tmp_df = data_test[['Age','Fare','Parch','SibSp','Pclass']]
null_age = tmp_df[data_test.Age.isnull()].values
#根据特征属性X预测年龄并补上
X=null_age[:,1:]

predictedAges =rfr.predict(X)
data_test.loc[(data_test.Age.isnull()),'Age']=predictedAges
data_test =set_Cabin_type(data_test)

dummies_Cabin =pd.get_dummies(data_test['Cabin'],prefix='Cabin')
dummies_Embarked =pd.get_dummies(data_test['Embarked'],prefix='Embarked')
dummies_Sex =pd.get_dummies(data_test['Sex'],prefix='Sex')
dummies_Pclass =pd.get_dummies(data_test['Pclass'],prefix='Pclass')

df_test =pd.concat([data_test, dummies_Cabin,dummies_Embarked,dummies_Sex, dummies_Pclass],axis=1)
df_test.drop(['Pclass','Name','Sex','Ticket','Cabin','Embarked'],axis=1,inplace=True)
df_test['Age_scaled']= scaler.fit_transform(df_test['Age'].values.reshape(-1,1),age_scale_param)
df_test['Fare_scaled']=scaler.fit_transform(df_test['Fare'].values.reshape(-1,1),fare_scale_param)
df_test.head(10)

test = df_test.filter(regex='Age_.*|SibSp|Parch|Fare._*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
print(test)
test=test.values
print(test)
predictions =clf.predict(test)

result =pd.DataFrame({'PassengerId':data_test['PassengerId'].values,'Survived':predictions.astype(np.int32)})
result.to_csv("./logistic_regression_predictions.csv",index=False)

test = df_test.filter(regex='Age_.*|SibSp|Parch|Fare._*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
test=test.values
predictions =clf.predict(test)

result =pd.DataFrame({'PassengerId':data_test['PassengerId'].values,'Survived':predictions.astype(np.int32)})
result.to_csv("./logistic_regression_predictions.csv",index=False)

#查看已经保存的预测结果
pd.read_csv("./logistic_regression_predictions.csv")
# 计算存活和未存活人数
survival_counts = result['Survived'].value_counts()
print(survival_counts)

#5.1模型系数关联分析——LR模型系数
df51=pd.DataFrame ({"columns":list(train_df. columns)[1:],"coef":list(clf.coef_.T)})
print(df51)

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.linear_model import LinearRegression
# 初始化线性回归模型
clf = LinearRegression()
# 获取数据集
all_data = df.filter(regex='Survived|Age_.*|SibSp|Parch|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
# 提取特征和标签
x = all_data.values[:, 1:]  # 从第二列开始提取特征
y = all_data.values[:, 0]   # 提取标签（Survived）
# 进行交叉验证
print(cross_val_score(clf, x, y, cv=5))

from sklearn.metrics import mean_squared_error
# 分割数据，按照训练数据:交叉验证数据=7:3的比例
split_train, split_cv = train_test_split(df, test_size=0.3, random_state=42)
train_df = split_train.filter(regex='Survived|Age_.*|SibSp|Parch|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass.*')
# 生成模型
clf = LinearRegression()
clf.fit(train_df.values[:, 1:], train_df.values[:, 0])
# 对交叉验证数据进行预测
cv_df = split_cv.filter(regex='Survived|Age_.*|SibSp|Parch|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass.*')
predictions = clf.predict(cv_df.values[:, 1:])
# 计算均方误差
mse = mean_squared_error(cv_df.values[:, 0], predictions)
print(f"Mean Squared Error: {mse}")
# 读取原始数据
origin_data_train = pd.read_csv("train.csv")
# 查找预测错误的案例
bad_cases = origin_data_train.loc[origin_data_train['PassengerId'].isin(split_cv[predictions != cv_df.values[:, 0]]['PassengerId'].values)]
# 显示前10个错误案例
bad_cases.head(10)

#绘制学习曲线
#获得bad_cases之后，通过绘制学习曲线，判定我们的模型现在所处的状态属于欠拟合还是过拟合状态
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
#此题中用错误率代表得分
#用sklearn的learning_curve得到training_score和cv_score,使用matplotlib画出learning curve
def plot_learning_curve(estimator, title,x,y,ylim=None,cv=None,n_jobs=1,train_sizes=np.linspace(.05,1.,20),verbose=0,plot=True):
    train_sizes,train_scores,test_scores=learning_curve(estimator,x,y,cv=cv,n_jobs=n_jobs,train_sizes=train_sizes, verbose=verbose)
    train_scores_mean=np.mean(train_scores,axis=1)
    train_scores_std=np.std(train_scores,axis=1)
    test_scores_mean =np.mean(test_scores, axis=1)
    test_scores_std=np.std(test_scores,axis=1)
    if plot:
        plt.figure()
        plt.title(title)
        if ylim is not None:
            plt.ylim(*ylim)
        plt.xlabel( 'train_sample_counts ')
        plt.ylabel( 'score' )
        plt.gca().invert_yaxis()
        plt.grid()
        plt.fill_between(train_sizes, train_scores_mean - train_scores_std,train_scores_mean + train_scores_std,
                         alpha=0.1,color="b")
        plt.fill_between(train_sizes, test_scores_mean- test_scores_std, test_scores_mean + test_scores_std,
                         alpha=0.1,color='r')
        plt.plot(train_sizes,train_scores_mean,'o-',color="b", label="score on train data")
        plt.plot(train_sizes,test_scores_mean,'o-', color="r", label="score on cv data")
        plt.legend(loc="best")
        plt.draw()
        plt.gca().invert_yaxis()
        plt.show()

    midpoint = ((train_scores_mean[-1]+ train_scores_std[-1])+ (test_scores_mean[-1]- test_scores_std[-1]))/2
    diff= (train_scores_mean[-1]+ train_scores_std[-1])-(test_scores_mean[-1]- test_scores_std[-1])
    return midpoint, diff
plot_learning_curve(clf,"learning cruves",x,y)