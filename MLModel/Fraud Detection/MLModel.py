from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
from ModelStorage import ModelStorage
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix, precision_score, recall_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

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

        training_data_table_name="Fraud Detection Train Revised"
        columns=["age","amt","category","cc_num","city","city_pop","dob","first","gender","ID","is_fraud","job","last","lat","long","merchant","merch_lat","merch_long","state","street","trans_date_trans_time","trans_num","unix_time","zip"]
        target_column='is_fraud'
        datetime_column = 'trans_date_trans_time'
        model_name='churn_prediction_model'
        resultant_column_name='Prediction'
        directory = 'models'

        df: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(training_data_table_name, columns,"")
        
        df[datetime_column] = pd.to_datetime(df[datetime_column])
        df['Year'] = df[datetime_column].dt.year
        df['Month'] = df[datetime_column].dt.month
        df['Day'] = df[datetime_column].dt.day
        df['Hour'] = df[datetime_column].dt.hour

        # Drop the original datetime column if it's not needed
        df.drop(datetime_column, axis=1, inplace=True)

        # Split features and target
        X = df.drop(target_column, axis=1)
        y = df[target_column]

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Define the preprocessing for numerical and categorical data
        numerical_features = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_features = X_train.select_dtypes(include=['object']).columns.tolist()

        # Add SimpleImputer to handle missing values
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', Pipeline(steps=[
                    ('imputer', SimpleImputer(strategy='mean')),  # Fill NaNs in numerical features with the mean
                    ('scaler', StandardScaler())
                ]), numerical_features),
                ('cat', Pipeline(steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),  # Fill NaNs in categorical features with the most frequent value
                    ('encoder', OneHotEncoder(handle_unknown='ignore'))
                ]), categorical_features)
            ]
        )

        # Define the model pipeline
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(random_state=42))
        ])
        #Train Model
        # Fit the model
        model.fit(X_train, y_train)
        #Test Trained Model
        # Predict on the test set
        y_pred = model.predict(X_test)
        #Save Trained Model
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)

        # Print evaluation metrics
        self.log.INFO(f"Accuracy: {accuracy:.4f}")
        self.log.INFO(f"F1 Score: {f1:.4f}")
        self.log.INFO(f"Precision: {precision:.4f}")
        self.log.INFO(f"Recall: {recall:.4f}")
        self.log.INFO(f"Confusion Matrix:\n{conf_matrix}")
        file_path = os.path.join(directory, 'model.pkl')
        os.makedirs(directory, exist_ok=True)
        joblib.dump(model, file_path)
        self.ms.store_model('model', file_path)
        self.ms.list_models()
        self.log.INFO("Training Completed...Procced to Predict")

    def predict(self):

        training_data_table_name="Fraud Detection Test Revised"
        columns=["age", "amt", "category", "cc_num", "city", "city_pop", "dob", "first", "gender", "ID", "job", "last", 
             "lat", "long", "merchant", "merch_lat", "merch_long", "state", "street", "trans_date_trans_time", 
             "trans_num", "unix_time", "zip"]
        resultant_column_name='Prediction'
        resultant_table_name="Predicted Fraud Transactions Revised"
        import_type="truncateadd"
        datetime_column = 'trans_date_trans_time'

        # Fetch the saved model from storage
        pkl_file_path = self.ms.get_model_path('model')

        # Load the model from the .pkl file
        model = joblib.load(pkl_file_path)
        
        # Fetch new data for prediction
        new_data: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(training_data_table_name,columns,"")

        # Convert the datetime column to features if it's present
        
        if datetime_column in new_data.columns:
            new_data[datetime_column] = pd.to_datetime(new_data[datetime_column])
            new_data['Year'] = new_data[datetime_column].dt.year
            new_data['Month'] = new_data[datetime_column].dt.month
            new_data['Day'] = new_data[datetime_column].dt.day
            new_data['Hour'] = new_data[datetime_column].dt.hour

            # Drop the original datetime column if it's not needed
            new_data.drop(datetime_column, axis=1, inplace=True)

        # Ensure the new data has the same features as the training data
        X_new = new_data

        # Use the loaded model to predict
        predictions = model.predict(X_new)

        # Optionally, log or print the predictions
        prediction_output = pd.DataFrame({'ID': new_data['ID'], 'is_fraud': predictions})
        self.log.INFO("Predictions:")
        self.log.INFO(prediction_output)

        output = pd.DataFrame({'ID': new_data['ID'], resultant_column_name: predictions})

        # Upload the predictions back to Zoho Analytics
        self.dt.upload_tabledata_from_DataFrame(resultant_table_name, output, {"importType": import_type})
