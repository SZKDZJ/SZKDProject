import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import lightgbm as lgb

# Load data
train_data = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")

# Fill missing 'Age' based on 'Pclass' and 'Sex' median values
train_data['Age'] = train_data.groupby(['Pclass', 'Sex'])['Age'].transform(lambda x: x.fillna(x.median()))
test_data['Age'] = test_data.groupby(['Pclass', 'Sex'])['Age'].transform(lambda x: x.fillna(x.median()))

# Fill missing 'Embarked' with the mode in train_data
train_data['Embarked'] = train_data['Embarked'].fillna(train_data['Embarked'].mode()[0])

# Fill missing 'Fare' in test_data with the median
test_data['Fare'] = test_data['Fare'].fillna(test_data['Fare'].median())

# Extract Title from Name
for df in [train_data, test_data]:
    df['Title'] = df['Name'].apply(lambda x: x.split(',')[1].split('.')[0].strip())

# Simplify titles into broader categories
title_mapping = {
    "Mr": "Mr", "Miss": "Miss", "Mrs": "Mrs", "Master": "Master",
    "Dr": "Officer", "Rev": "Officer", "Col": "Officer", "Major": "Officer",
    "Mlle": "Miss", "Countess": "Royalty", "Ms": "Miss", "Lady": "Royalty",
    "Jonkheer": "Royalty", "Don": "Royalty", "Mme": "Mrs", "Capt": "Officer",
    "Sir": "Royalty"
}
for df in [train_data, test_data]:
    df['Title'] = df['Title'].map(title_mapping)

# Create FamilySize feature
for df in [train_data, test_data]:
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1

# Extract first letter of Cabin as a feature (if available), otherwise 'X'
for df in [train_data, test_data]:
    df['Cabin'] = df['Cabin'].fillna('X').apply(lambda x: x[0])

# Encode categorical features: Sex, Embarked, Title, and Cabin
label_encoder = LabelEncoder()
for col in ['Sex', 'Embarked', 'Title', 'Cabin']:
    train_data[col] = label_encoder.fit_transform(train_data[col])
    test_data[col] = label_encoder.transform(test_data[col])

# Select features and target
features = ['Pclass', 'Sex', 'Age', 'Fare', 'FamilySize', 'Embarked', 'Title', 'Cabin']
X = train_data[features]
y = train_data['Survived']
X_test = test_data[features]

# Standardize numeric features
scaler = StandardScaler()
X[['Age', 'Fare']] = scaler.fit_transform(X[['Age', 'Fare']])
X_test[['Age', 'Fare']] = scaler.transform(X_test[['Age', 'Fare']])

# Split data
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Hyperparameter tuning for RandomForest
param_grid_rf = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10],
    'class_weight': ['balanced']
}
grid_rf = GridSearchCV(RandomForestClassifier(random_state=42), param_grid_rf, cv=5, scoring='accuracy', n_jobs=-1)
grid_rf.fit(X_train, y_train)
best_rf = grid_rf.best_estimator_

# Hyperparameter tuning for XGBoost
param_grid_xgb = {
    'n_estimators': [100, 200],
    'max_depth': [3, 6, 9],
    'learning_rate': [0.01, 0.05, 0.1],
    'subsample': [0.6, 0.8, 1.0]
}
grid_xgb = GridSearchCV(xgb.XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='mlogloss'),
                        param_grid_xgb, cv=5, scoring='accuracy', n_jobs=-1)
grid_xgb.fit(X_train, y_train)
best_xgb = grid_xgb.best_estimator_

# Hyperparameter tuning for LightGBM
param_grid_lgb = {
    'n_estimators': [100, 200],
    'max_depth': [5, 10, 15],
    'feature_fraction': [0.6, 0.8, 1.0]
}
grid_lgb = GridSearchCV(lgb.LGBMClassifier(random_state=42), param_grid_lgb, cv=5, scoring='accuracy', n_jobs=-1)
grid_lgb.fit(X_train, y_train)
best_lgb = grid_lgb.best_estimator_

# Voting Classifier with optimized parameters
voting_clf = VotingClassifier(estimators=[
    ('rf', best_rf),
    ('xgb', best_xgb),
    ('lgb', best_lgb)
], voting='soft')

# Cross-validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(voting_clf, X_train, y_train, cv=cv, scoring='accuracy')
print(f"Cross-validated accuracy: {cv_scores.mean():.2f}")

# Train and evaluate on validation set
voting_clf.fit(X_train, y_train)
y_pred = voting_clf.predict(X_val)

# Evaluation metrics
accuracy = accuracy_score(y_val, y_pred)
precision = precision_score(y_val, y_pred)
recall = recall_score(y_val, y_pred)
f1 = f1_score(y_val, y_pred)

print(f"Validation Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}, Recall: {recall:.2f}, F1 Score: {f1:.2f}")

# 7. Predict on test set and save submission file
y_test_pred = voting_clf.predict(X_test)

output = pd.DataFrame({'PassengerId': test_data['PassengerId'], 'Survived': y_test_pred})
output.to_csv('submission.csv', index=False)
print("预测结果已保存到submission.csv")
