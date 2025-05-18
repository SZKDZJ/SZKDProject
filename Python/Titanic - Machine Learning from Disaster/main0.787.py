import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, AdaBoostClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import xgboost as xgb
import lightgbm as lgb

# Load data
train_data = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")


# Feature Engineering
def create_features(data):
    # Fill missing 'Age' based on 'Pclass' and 'Sex' median values
    data['Age'] = data.groupby(['Pclass', 'Sex'])['Age'].transform(lambda x: x.fillna(x.median()))

    # Fill missing 'Embarked' with the mode
    data['Embarked'] = data['Embarked'].fillna(data['Embarked'].mode()[0])

    # Fill missing 'Fare' with the median
    data['Fare'] = data['Fare'].fillna(data['Fare'].median())

    # Extract Title from Name
    data['Title'] = data['Name'].apply(lambda x: x.split(',')[1].split('.')[0].strip())

    # Simplify titles into broader categories
    title_mapping = {
        "Mr": "Mr", "Miss": "Miss", "Mrs": "Mrs", "Master": "Master",
        # Other titles...
    }
    data['Title'] = data['Title'].map(title_mapping)

    # Create FamilySize feature
    data['FamilySize'] = data['SibSp'] + data['Parch'] + 1

    # Extract first letter of Cabin as a feature
    data['Cabin'] = data['Cabin'].fillna('X').apply(lambda x: x[0])

    # Create binary features for Deck (Cabin letter)
    deck = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "T": 8}
    data['Deck'] = data['Cabin'].map(deck)
    data['Deck'] = data['Deck'].fillna(0)

    return data


train_data = create_features(train_data)
test_data = create_features(test_data)

# Encode categorical features
categorical_features = ['Sex', 'Embarked', 'Title', 'Cabin', 'Deck']
label_encoder = LabelEncoder()
for col in categorical_features:
    train_data[col] = label_encoder.fit_transform(train_data[col])
    test_data[col] = label_encoder.transform(test_data[col])

# Select features and target
features = ['Pclass', 'Sex', 'Age', 'Fare', 'FamilySize', 'Embarked', 'Title', 'Cabin', 'Deck']
X = train_data[features]
y = train_data['Survived']
X_test = test_data[features]

# Split data
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Preprocessing pipeline
numeric_features = ['Age', 'Fare', 'FamilySize', 'Deck']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

categorical_features = ['Pclass', 'Sex', 'Embarked', 'Title', 'Cabin']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])


# Model training and hyperparameter tuning
def train_model(X_train, y_train, X_val, y_val):
    # RandomForest
    rf = RandomForestClassifier(random_state=42)
    param_grid_rf = {
        'n_estimators': [100, 200, 300],
        'max_depth': [5, 10, 15],
        'min_samples_split': [2, 5, 10],
        'class_weight': ['balanced']
    }
    grid_rf = GridSearchCV(rf, param_grid_rf, cv=5, scoring='accuracy', n_jobs=-1)
    grid_rf.fit(X_train, y_train)
    best_rf = grid_rf.best_estimator_

    # XGBoost
    xgb_clf = xgb.XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='mlogloss')
    param_grid_xgb = {
        'n_estimators': [100, 200],
        'max_depth': [3, 6, 9],
        'learning_rate': [0.01, 0.05, 0.1],
        'subsample': [0.6, 0.8, 1.0]
    }
    grid_xgb = GridSearchCV(xgb_clf, param_grid_xgb, cv=5, scoring='accuracy', n_jobs=-1)
    grid_xgb.fit(X_train, y_train)
    best_xgb = grid_xgb.best_estimator_

    # LightGBM
    lgb_clf = lgb.LGBMClassifier(random_state=42)
    param_grid_lgb = {
        'n_estimators': [100, 200],
        'max_depth': [5, 10, 15],
        'feature_fraction': [0.6, 0.8, 1.0]
    }
    grid_lgb = GridSearchCV(lgb_clf, param_grid_lgb, cv=5, scoring='accuracy', n_jobs=-1)
    grid_lgb.fit(X_train, y_train)
    best_lgb = grid_lgb.best_estimator_

    # Voting Classifier
    voting_clf = VotingClassifier(estimators=[
        ('rf', best_rf),
        ('xgb', best_xgb),
        ('lgb', best_lgb)
    ], voting='soft')
    voting_clf.fit(X_train, y_train)

    return voting_clf


# Train the model
model = train_model(X_train, y_train, X_val, y_val)

# Evaluation
y_pred = model.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)
precision = precision_score(y_val, y_pred)
recall = recall_score(y_val, y_pred)
f1 = f1_score(y_val, y_pred)

print(f"Validation Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}, Recall: {recall:.2f}, F1 Score: {f1:.2f}")

# Predict on test set and save submission file
y_test_pred = model.predict(X_test)

output = pd.DataFrame({'PassengerId': test_data['PassengerId'], 'Survived': y_test_pred})
output.to_csv('submission.csv', index=False)
print("预测结果已保存到submission.csv")
