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
        table_name = "CRM Deal Prediction Train Data"
        column_names =  ['Deal ID', 'Amount', 'Deal Name', 'Closing Date',
                                                                 'Stage', 'Type',
                                                                 'Probability (%)', 'Expected Revenue', 'Lead Source',
                                                                 'Created Time',
                                                                 'Modified Time', 'Sales Cycle Duration']
        df: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)


        df.drop(['Deal ID', 'Deal Name', 'Created Time', 'Modified Time', 'Closing Date'], axis=1, inplace=True)

        # df.isna().sum()

        df['Type'] = df['Type'].fillna('Type Not Mentioned')
        df['Lead Source'] = df['Lead Source'].fillna('Lead Not Mentioned')
        # df.isna().sum()

        # df.duplicated().sum()

        Type_Values = list(df['Type'].unique())

        Lead_Source_Values = list(df['Lead Source'].unique())

        Type = pd.get_dummies(df['Type']).astype(int)
        Lead_Source = pd.get_dummies(df['Lead Source']).astype(int)
        df.drop(['Type', 'Lead Source'], axis=1, inplace=True)
        df = pd.concat([df, Type, Lead_Source], axis=1)

        df['Stage'] = df['Stage'].apply(lambda x: 1 if x == 'Closed Won' else 0)

        # df['Stage'].value_counts()

        # df.corr()['Stage'].sort_values(ascending = False)

        X = df.drop('Stage', axis=1)
        y = df['Stage']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

        train_data = lgb.Dataset(X_train, label=y_train)
        test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

        params = {
            'objective': 'binary',  # For binary classification
            'boosting_type': 'gbdt',  # Gradient Boosting Decision Tree
            'metric': ['binary_logloss', 'auc'],  # Metrics to evaluate
            'num_leaves': 31,  # Maximum number of leaves in one tree
            'learning_rate': 0.01,  # Learning rate
            'feature_fraction': 0.9,  # Fraction of features to use for building each tree
            'verbose': 0  # Verbosity level
        }

        model = lgb.train(params,
                          train_data,
                          num_boost_round=100,
                          valid_sets=[train_data, test_data],
                          valid_names=['train', 'valid'])

        y_pred = model.predict(X_test, num_iteration=model.best_iteration)
        y_pred_binary = [1 if x > 0.5 else 0 for x in y_pred]

        accuracy = accuracy_score(y_test, y_pred_binary)
        self.log.INFO(accuracy)

        conf_matrix = confusion_matrix(y_test, y_pred_binary)
        classification = classification_report(y_test, y_pred_binary)
        roc_auc = roc_auc_score(y_test, y_pred_binary)
        # print(f"ROC AUC Score: {roc_auc:.4f}")
        self.log.INFO(conf_matrix)
        # print(f"Classification Report:\n{classification}")

        X_test.reset_index(drop=True, inplace=True)
        y_test.reset_index(drop=True, inplace=True)

        X_test['Type'] = X_test[Type_Values].idxmax(axis=1)
        X_test['Lead_Source'] = X_test[Lead_Source_Values].idxmax(axis=1)
        X_test.drop(Type_Values, axis=1, inplace=True)
        X_test.drop(Lead_Source_Values, axis=1, inplace=True)

        output = pd.DataFrame({'Deal Prediction': y_pred_binary})
        output = pd.concat([X_test, y_test, output], axis=1)

        self.log.INFO(output)
        # Save Trained Model
        directory = 'models'
        file_path = os.path.join(directory, 'lgb_clf_deal_pred.pkl')
        os.makedirs(directory, exist_ok=True)
        joblib.dump(model, file_path)
        self.ms.store_model('lgb_clf_deal_pred', file_path)
        self.ms.list_models()
        self.log.INFO("Training Completed...Procced to Predict")

    def predict(self):
        table_name = "CRM Deal Prediction Validation Data"
        column_names =  ['Deal ID', 'Amount', 'Deal Name', 'Closing Date',
                                                                 'Stage', 'Type',
                                                                 'Probability (%)', 'Expected Revenue', 'Lead Source',
                                                                 'Created Time',
                                                                 'Modified Time', 'Sales Cycle Duration']
        final_table_name = "CRM Deal Predicted Data"
        import_type = "truncateadd"
        # Path to the .pkl file
        pkl_file_path = self.ms.get_model_path('lgb_clf_deal_pred')
        # Load the model from the .pkl file
        model = joblib.load(pkl_file_path)

        df: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)


        df.drop(['Deal ID', 'Deal Name', 'Created Time', 'Modified Time', 'Closing Date'], axis=1, inplace=True)

        # df.isna().sum()

        df['Type'] = df['Type'].fillna('Type Not Mentioned')
        df['Lead Source'] = df['Lead Source'].fillna('Lead Not Mentioned')
        # df.isna().sum()

        # df.duplicated().sum()

        Type_Values = ['New Business', 'Existing Business', 'Type Not Mentioned']

        Lead_Source_Values = ['Advertisement', 'Partner', 'Lead Not Mentioned', 'Lead Source', 'Employee Referral',
                              'Online Store', 'Seminar Partner', 'External Referral', 'Sales Email Alias',
                              'Web Download', 'Public Relations', 'Internal Seminar',
                              'Facebook', 'Chat', 'Cold Call', 'Trade Show', 'Google+', 'Web Research', 'Twitter']

        Type = pd.get_dummies(df['Type']).astype(int)
        Lead_Source = pd.get_dummies(df['Lead Source']).astype(int)

        df.drop(['Type', 'Lead Source'], axis=1, inplace=True)
        df = pd.concat([df, Type, Lead_Source], axis=1)

        # creating columns for categories that are missing but the model requires since it was trained on them
        for i in Type_Values:
            if i not in df.columns:
                df[i] = 0

        for i in Lead_Source_Values:
            if i not in df.columns:
                df[i] = 0

        df['Stage'] = df['Stage'].apply(lambda x: 1 if x == 'Closed Won' else 0)

        # df['Stage'].value_counts()

        # df.corr()['Stage'].sort_values(ascending = False)

        X = df.drop('Stage', axis=1)
        y = df['Stage']

        y_pred = model.predict(X, num_iteration=model.best_iteration)
        y_pred_binary = [1 if x > 0.5 else 0 for x in y_pred]

        accuracy = accuracy_score(y, y_pred_binary)
        self.log.INFO(accuracy)

        X.reset_index(drop=True, inplace=True)
        y.reset_index(drop=True, inplace=True)

        X['Type'] = X[Type_Values].idxmax(axis=1)
        X['Lead_Source'] = X[Lead_Source_Values].idxmax(axis=1)
        X.drop(Type_Values, axis=1, inplace=True)
        X.drop(Lead_Source_Values, axis=1, inplace=True)

        output = pd.DataFrame({'Deal Prediction': y_pred_binary})
        output = pd.concat([X, y, output], axis=1)

        output['Stage'] = output['Stage'].apply(lambda x: 'Yes' if x == 0 else 'No').astype('string')
        output['Deal Prediction'] = output['Deal Prediction'].apply(lambda x: 'Yes' if x == 0 else 'No').astype(
            'string')
        output['Type'] = output['Type'].astype('string')
        output['Lead_Source'] = output['Lead_Source'].astype('string')

        self.log.INFO(output)

        # Now, 'model' contains the deserialized machine learning model
        # You can use the loaded model to make predictions or evaluate it
        # Example usage: Making predictions with the loaded model
        # Assuming you have test data in the variable 'X_test'
        self.dt.upload_tabledata_from_DataFrame(final_table_name, output, {"importType": import_type})