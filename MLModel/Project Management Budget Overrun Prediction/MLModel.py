from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
from ModelStorage import ModelStorage
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score
import joblib
import os


class MLModel:
    dt: DataTransformationUtil = None
    za: ZohoAnalytics = None
    ms: ModelStorage = None

    def __init__(self, za, ms):
        self.za = za
        self.dt = DataTransformationUtil(self.za)
        self.log = self.za.context.log
        self.ms = ms

    def fit(self):
        df: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame("Project Management Data",
                                                                ['Budget', 'NumAgents', 'ProjectType', 'Location',
                                                                 'ClientType',
                                                                 'PlannedHours', 'PlannedDays', 'ActualHours',
                                                                 'ActualDays', 'NumIssues',
                                                                 'ProjectDifficulty', 'Urgency', 'ScopeChanges',
                                                                 'TeamExperienceLevel',
                                                                 'VendorReliabilityCategory', 'MarketFluctuation',
                                                                 'BudgetOverrun'], "")
        # df.isna().sum()

        # df.duplicated().sum()

        # dropping unnecessary columns
        df.drop(['ProjectType', 'Location', 'ClientType'], axis=1, inplace=True)

        # label encoding
        encoding_order = ['Low', 'Medium', 'High']
        df['TeamExperienceLevel'] = df['TeamExperienceLevel'].apply(lambda x: encoding_order.index(x))
        df['VendorReliabilityCategory'] = df['VendorReliabilityCategory'].apply(lambda x: encoding_order.index(x))
        # df.head()
        correlation = pd.DataFrame(df.corr())
        correlation['columns'] = df.columns
        correlation['columns'] = correlation['columns'].astype('string')

        self.dt.upload_tabledata_from_DataFrame("Correlation Matrix", correlation, {"importType": "truncateadd"})

        self.log.INFO(correlation)

        X = df.drop(['BudgetOverrun'], axis=1)
        y = df['BudgetOverrun']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
        X_train.shape, X_test.shape, y_train.shape, y_test.shape

        train_data = lgb.Dataset(X_train, label=y_train)
        test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

        params = {
            'objective': 'binary',  # For binary classification
            'boosting_type': 'gbdt',  # Gradient Boosting Decision Tree
            'metric': ['binary_logloss', 'auc'],  # Metrics to evaluate
            'num_leaves': 31,  # Maximum number of leaves in one tree
            'learning_rate': 0.05,  # Learning rate
            'feature_fraction': 0.9,  # Fraction of features to use for building each tree
            'verbose': 0  # Verbosity level
        }

        gbm = lgb.train(
            params,
            train_data,
            num_boost_round=100,  # Number of boosting iterations
            valid_sets=[train_data, test_data],  # Validation sets to monitor performance
            valid_names=['train', 'valid'],  # Names for training and validation data
        )

        y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
        y_pred_binary = [1 if x > 0.5 else 0 for x in y_pred]

        accuracy = accuracy_score(y_test, y_pred_binary)
        self.log.INFO(accuracy)
        conf_matrix = confusion_matrix(y_test, y_pred_binary)
        classification = classification_report(y_test, y_pred_binary)
        roc_auc = roc_auc_score(y_test, y_pred_binary)
        # print(f"ROC AUC Score: {roc_auc:.4f}")
        # print(f"Confusion Matrix:\n{conf_matrix}")
        # print(f"Classification Report:\n{classification}")

        X_test.reset_index(drop=True, inplace=True)
        y_test.reset_index(drop=True, inplace=True)
        output = pd.DataFrame({'Predicted_Budget_Overrun': y_pred_binary})
        output = pd.concat([X_test, y_test, output], axis=1)

        self.log.INFO(output)
        # Save Trained Model
        directory = 'models'
        file_path = os.path.join(directory, 'lgbBudgetOverrunClassifier.pkl')
        os.makedirs(directory, exist_ok=True)
        joblib.dump(gbm, file_path)
        self.ms.store_model('lgbBudgetOverrunClassifier', file_path)
        self.ms.list_models()
        self.log.INFO("Training Completed...Procced to Predict")

    def predict(self):
        # Path to the .pkl file
        pkl_file_path = self.ms.get_model_path('lgbBudgetOverrunClassifier')
        # Load the model from the .pkl file
        model = joblib.load(pkl_file_path)
        df: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame("Project Management Validation Data",
                                                                ['Budget', 'NumAgents', 'ProjectType', 'Location',
                                                                 'ClientType',
                                                                 'PlannedHours', 'PlannedDays', 'ActualHours',
                                                                 'ActualDays', 'NumIssues',
                                                                 'ProjectDifficulty', 'Urgency', 'ScopeChanges',
                                                                 'TeamExperienceLevel',
                                                                 'VendorReliabilityCategory', 'MarketFluctuation',
                                                                 'BudgetOverrun'], "")

        df.drop(['ProjectType', 'Location', 'ClientType'], axis=1, inplace=True)
        encoding_order = ['Low', 'Medium', 'High']
        df['TeamExperienceLevel'] = df['TeamExperienceLevel'].apply(lambda x: encoding_order.index(x))
        df['VendorReliabilityCategory'] = df['VendorReliabilityCategory'].apply(lambda x: encoding_order.index(x))

        X = df.drop(['BudgetOverrun'], axis=1)
        y = df['BudgetOverrun']

        y_pred = model.predict(X, num_iteration=model.best_iteration)
        y_pred_binary = [1 if x > 0.5 else 0 for x in y_pred]

        accuracy = accuracy_score(y, y_pred_binary)
        self.log.INFO(accuracy)

        X.reset_index(drop=True, inplace=True)
        y.reset_index(drop=True, inplace=True)
        output = pd.DataFrame({'Predicted_Budget_Overrun': y_pred_binary})
        output = pd.concat([X, y, output], axis=1)

        output['TeamExperienceLevel'] = output['TeamExperienceLevel'].apply(lambda x: encoding_order[x]).astype(
            'string')
        output['VendorReliabilityCategory'] = output['VendorReliabilityCategory'].apply(
            lambda x: encoding_order[x]).astype('string')
        output['BudgetOverrun'] = output['BudgetOverrun'].apply(lambda x: 'Yes' if x == 1 else 'No').astype('string')
        output['Predicted_Budget_Overrun'] = output['Predicted_Budget_Overrun'].apply(
            lambda x: 'Yes' if x == 1 else 'No').astype('string')
        self.log.INFO(output)

        self.dt.upload_tabledata_from_DataFrame("ProjectMgmtBudgetOverrunPred", output, {"importType": "truncateadd"})