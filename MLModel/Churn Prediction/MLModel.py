from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
from ModelStorage import ModelStorage
import joblib
import os
from pandas import DataFrame
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import xgboost as xgb
from sklearn.metrics import classification_report


class MLModel:
    dt: DataTransformationUtil = None
    za: ZohoAnalytics = None
    ms: ModelStorage = None

    def __init__(self, za,ms):
        self.za = za
        self.dt = DataTransformationUtil(self.za)
        self.log = self.za.context.log
        self.ms = ms

    def fit(self):
        training_data_table_name="CommData"
        columns=["ID","Tenure", "NumberOfDeviceRegistered", "SatisfactionScore","NumberOfAddress", "DaySinceLastOrder", "CashbackAmount","Churn","MaritalStatus", "PreferedOrderCat"]
        target_column="Churn"
        model_name='churn_prediction_model'
        resultant_column_name='Prediction'

        data: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(training_data_table_name, columns, "")

        label_encoders = {}
        for column in ["MaritalStatus", "PreferedOrderCat"]:
            le = LabelEncoder()
            data[column] = le.fit_transform(data[column])
            label_encoders[column] = le

        data.fillna(data.median(), inplace=True)

        X = data.drop(target_column, axis=1)
        y = data[target_column]

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Instantiate and train XGBoost model
        model = xgb.XGBClassifier()
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        output = pd.DataFrame({resultant_column_name: y_pred})
        self.log.INFO(output)

        # Evaluate the model
        print(classification_report(y_test, y_pred))
        #Save Trained Model
        directory = 'models'
        os.makedirs(directory, exist_ok=True)

        # Save the model
        model_path = os.path.join(directory, model_name+'.pkl')
        joblib.dump(model, model_path)
            
        self.ms.store_model(model_name, model_path)

        self.log.INFO("Training Completed...Proceed to Predict")

    def predict(self):
        # Path to the 'models' directory
        directory = 'models'
        training_data_table_name="newCommData"
        columns=["ID", "Tenure", "NumberOfDeviceRegistered", "SatisfactionScore","NumberOfAddress", "DaySinceLastOrder", "CashbackAmount", "Churn", "MaritalStatus", "PreferedOrderCat"]
        target_column="Churn"
        model_name='churn_prediction_model'
        resultant_column_name='Prediction'
        resultant_table_name="churn_predictions"
        import_type="truncateadd"

        # list models 
        self.ms.list_models()

        # Load the model
        model_path = self.ms.get_model_path(model_name)
        model = joblib.load(model_path)
        
        new_data: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(training_data_table_name, columns, "")

        label_encoders = {}
        for column in ["MaritalStatus", "PreferedOrderCat"]:
            le = LabelEncoder()
            new_data[column] = le.fit_transform(new_data[column])
            label_encoders[column] = le

        for column, le in label_encoders.items():
            if column in new_data.columns:
                # Create a mask for unseen labels
                unseen_mask = ~new_data[column].isin(le.classes_)
                if unseen_mask.any():
                    # Assign unseen labels to a default value or category (e.g., -1 or the most frequent label)
                    new_data.loc[unseen_mask, column] = le.classes_[0]  # Replace with the first class
                new_data[column] = le.transform(new_data[column])

        # Handle missing values (same strategy as used for the training data)
        new_data.fillna(new_data.median(), inplace=True)  # Use the same median values as before

        # Prepare the features for prediction
        X_new = new_data.drop(target_column, axis=1, errors="ignore")  # Drop "Churn" if it exists in the new data

        # Predict churn using the trained model
        y_pred_new = model.predict(X_new)

        output = pd.DataFrame({'ID': new_data.ID,resultant_column_name: y_pred_new})

        self.dt.upload_tabledata_from_DataFrame(resultant_table_name, output, {"importType": import_type})
