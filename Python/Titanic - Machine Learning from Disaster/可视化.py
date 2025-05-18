import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import category_encoders
from category_encoders import TargetEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import confusion_matrix,f1_score
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from imblearn.metrics import geometric_mean_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_curve,auc
from sklearn.svm import SVC
import toad

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

# 观察缺失值
(train.isna().sum()/train.shape[0]).apply(lambda x:format(x,'.2%'))

train.select_dtypes('O')

train.select_dtypes('number')



