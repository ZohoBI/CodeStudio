from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
from ModelStorage import ModelStorage
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix, precision_score, recall_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

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

        training_data_table_name="Maintenance Prediction"
        columns=["Air Temperature","Heat Dissipation Failure","Machine Failure","Overstrain Failure","Power Failure","Process Temperature","Product ID","Random Failure","Rotational Speed","Tool Wear Failure","Tool Wear","Torque","Type","Unique Identifier"]
        target_column = 'Machine Failure'
        model_name='maintenance_prediction_model'
        resultant_column_name='Prediction'
        directory = 'models'

        df: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(training_data_table_name,columns,"")

        # Print the columns to ensure they match the expected columns
        self.log.INFO(f"Dataset columns: {df.columns}")

        # Drop unnecessary columns
        df = df.drop(columns=['Unique Identifier', 'Product ID'])

        # Check if the target column exists
        if target_column not in df.columns:
            self.log.ERROR(f"Target column '{target_column}' not found in the dataset.")
            return

        # Define features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Define the preprocessing steps
        numerical_features = ['Air Temperature','Heat Dissipation Failure','Overstrain Failure','Power Failure','Process Temperature','Random Failure','Rotational Speed','Tool Wear Failure','Tool Wear','Torque']
        categorical_features = ['Type']

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numerical_features),
                ('cat', OneHotEncoder(), categorical_features)
            ]
        )

        # Define the model pipeline
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(random_state=42))
        ])

        # Train the model
        model.fit(X_train, y_train)

        # Make predictions on the test set
        y_pred = model.predict(X_test)

        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)

        # Log metrics
        self.log.INFO(f"Accuracy: {accuracy:.4f}")
        self.log.INFO(f"F1 Score: {f1:.4f}")
        self.log.INFO(f"Precision: {precision:.4f}")
        self.log.INFO(f"Recall: {recall:.4f}")
        self.log.INFO(f"Confusion Matrix:\n{conf_matrix}")

        # Save the trained model
        file_path = os.path.join(directory, model_name+'.pkl')
        os.makedirs(directory, exist_ok=True)
        joblib.dump(model, file_path)

        # Store the model in ModelStorage
        self.ms.store_model(model_name, file_path)
        self.ms.list_models()
        self.log.INFO("Training completed. Proceed to predict.")

    def predict(self):

        training_data_table_name="Maintenance Prediction Test"
        columns=["Air Temperature","Heat Dissipation Failure","Machine Failure","Overstrain Failure","Power Failure","Process Temperature","Product ID","Random Failure","Rotational Speed","Tool Wear Failure","Tool Wear","Torque","Type","Unique Identifier"]
        model_name='maintenance_prediction_model'
        resultant_column_name='Machine Maintenance'
        resultant_table_name="Predicted Machine Maintenance"
        import_type="truncateadd"

        # Load the saved model
        pkl_file_path = self.ms.get_model_path(model_name)
        model = joblib.load(pkl_file_path)

        # Load new data for prediction (replace with actual fetching method)
        new_data: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(training_data_table_name, columns,"")

        # Preprocess the new data as done during training
        predictions = model.predict(new_data)

        # Map 0 and 1 to "machine not failed" and "machine failed"
        prediction_labels = ['Maintenance Not Needed' if pred == 0 else 'Maintenance Needed' for pred in predictions]
        
        # Log or save predictions
        self.log.INFO("Predictions:")
        prediction_output = pd.DataFrame({'Unique Identifier': new_data['Unique Identifier'],'Product ID': new_data['Product ID'], resultant_column_name: prediction_labels})
        self.log.INFO(prediction_output)
        prediction_output[resultant_column_name] = prediction_output[resultant_column_name].astype('string[python]')

        # Upload the predictions (replace with actual upload method)
        self.dt.upload_tabledata_from_DataFrame(resultant_table_name, prediction_output, {"importType": import_type})
