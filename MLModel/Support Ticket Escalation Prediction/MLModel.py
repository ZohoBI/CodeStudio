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
        df: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame("Ticket Escalation Train Data",
                                                                ['TicketID', 'IssueType', 'Priority', 'ResponseTime',
                                                                 'ResolutionTime',
                                                                 'CustomerType', 'TicketAge', 'Escalated'], "")

        cust_type_unique = df['CustomerType'].unique()
        cust_type_unique

        # df.isna().sum()

        # df.duplicated().sum()

        df.drop(['IssueType', 'TicketID'], axis=1, inplace=True)

        priority_order = ['Low', 'Medium', 'High', 'Critical']
        df['Priority'] = df['Priority'].apply(lambda x: priority_order.index(x))

        CustomerType = pd.get_dummies(df['CustomerType']).astype(int)
        df = pd.concat([df, CustomerType], axis=1)
        df.drop(['CustomerType'], axis=1, inplace=True)

        X = df.drop(['Escalated'], axis=1)
        y = df['Escalated']

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
            'bagging_fraction': 0.8,  # Fraction of data to use for each boosting iteration
            'bagging_freq': 5,  # Perform bagging every 5 iterations
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

        # print(y_pred_binary)

        accuracy = accuracy_score(y_test, y_pred_binary)
        # print(f"Accuracy: {accuracy}")
        self.log.INFO(accuracy)
        conf_matrix = confusion_matrix(y_test, y_pred_binary)
        classification = classification_report(y_test, y_pred_binary)
        roc_auc = roc_auc_score(y_test, y_pred_binary)
        # print(f"ROC AUC Score: {roc_auc:.4f}")
        # print(f"Confusion Matrix:\n{conf_matrix}")
        # print(f"Classification Report:\n{classification}")

        predicted_df = pd.DataFrame({'Predicted_Escalated': y_pred_binary})

        X_test.reset_index(drop=True, inplace=True)
        y_test.reset_index(drop=True, inplace=True)
        predicted_df.reset_index(drop=True, inplace=True)

        X_test['Priority'] = X_test['Priority'].apply(lambda x: priority_order[x])  # decoding priority to actual values

        predicted_df = pd.concat([X_test, y_test, predicted_df], axis=1)

        predicted_df['CustomerType'] = predicted_df[cust_type_unique].idxmax(
            axis=1)  # de-OneHotEncoding Customer Type column

        predicted_df.drop(cust_type_unique, axis=1, inplace=True)

        predicted_df.head()
        self.log.INFO(predicted_df)
        # Save Trained Model
        directory = 'models'
        file_path = os.path.join(directory, 'lgbclassifier.pkl')
        os.makedirs(directory, exist_ok=True)
        joblib.dump(gbm, file_path)
        self.ms.store_model('lgbclassifier', file_path)
        self.ms.list_models()
        self.log.INFO("Training Completed...Procced to Predict")

    def predict(self):
        # Path to the .pkl file
        pkl_file_path = self.ms.get_model_path('lgbclassifier')
        # Load the model from the .pkl file
        model = joblib.load(pkl_file_path)
        df: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame("Ticket Escalation Validation Data",
                                                                ['TicketID', 'IssueType', 'Priority', 'ResponseTime',
                                                                 'ResolutionTime',
                                                                 'CustomerType', 'TicketAge', 'Escalated'], "")

        cust_type_unique = df['CustomerType'].unique()
        # dropping unnecessary columns
        df.drop(['IssueType', 'TicketID'], axis=1, inplace=True)

        # Label Encoding
        priority_order = ['Low', 'Medium', 'High', 'Critical']
        df['Priority'] = df['Priority'].apply(lambda x: priority_order.index(x))

        # One Hot Encoding
        CustomerType = pd.get_dummies(df['CustomerType']).astype(int)
        df = pd.concat([df, CustomerType], axis=1)
        df.drop(['CustomerType'], axis=1, inplace=True)

        X = df.drop(['Escalated'], axis=1)
        y = df['Escalated']

        y_pred = model.predict(X, num_iteration=model.best_iteration)
        y_pred_binary = [1 if x > 0.5 else 0 for x in y_pred]

        accuracy = accuracy_score(y, y_pred_binary)
        self.log.INFO(accuracy)

        predicted_df = pd.DataFrame({'Predicted_Escalated': y_pred_binary})

        X.reset_index(drop=True, inplace=True)
        y.reset_index(drop=True, inplace=True)
        predicted_df.reset_index(drop=True, inplace=True)

        X['Priority'] = X['Priority'].apply(lambda x: priority_order[x]).astype(
            'string')  # decoding priority to actual values

        predicted_df = pd.concat([X, y, predicted_df], axis=1)

        predicted_df['CustomerType'] = predicted_df[cust_type_unique].idxmax(axis=1).astype(
            'string')  # de-OneHotEncoding Customer Type column

        predicted_df.drop(cust_type_unique, axis=1, inplace=True)

        self.log.INFO(predicted_df)
        self.dt.upload_tabledata_from_DataFrame("EscalationPredictedData", predicted_df, {"importType": "truncateadd"})