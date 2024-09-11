from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
from ModelStorage import ModelStorage
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib
import os


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
        training_data_table_name="Customer Segmentation Train"
        columns=["ID","Gender","Ever_Married","Age","Graduated","Profession","Work_Experience","Spending_Score","Family_Size","Var_1","Segmentation"]
        resultant_column_name='Predicted_Cluster'

        df: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(training_data_table_name, columns,"")
        # Select features for k-means clustering (excluding ID and Segmentation)
        features = df.drop(columns=['ID', 'Segmentation'])

        # One-hot encoding for categorical variables
        features_encoded = pd.get_dummies(features, columns=['Gender', 'Ever_Married', 'Graduated', 'Profession', 'Var_1'])

        # Standardize the feature values
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features_encoded)

        # Train k-means clustering model
        kmeans = KMeans(n_clusters=4, random_state=42)
        kmeans.fit(features_scaled)

        # Predict the clusters
        df[resultant_column_name] = kmeans.predict(features_scaled)

        output = pd.DataFrame({'ID': df.ID, resultant_column_name: df.Predicted_Cluster})
        self.log.INFO(output)

        #Save the model and scaler
        directory = 'models'
        file_path1 = os.path.join(directory, 'kmeans_model.pkl')
        file_path2 = os.path.join(directory, 'scaler.pkl')
        os.makedirs(directory, exist_ok=True)
        joblib.dump(kmeans, file_path1)
        joblib.dump(scaler, file_path2)
        self.ms.store_model('kmeans_model', file_path1)
        self.ms.store_model('scaler', file_path2)

        print("Model and scaler saved successfully.")
        
        self.ms.list_models()
        self.log.INFO("Training Completed...Procced to Predict")

    def predict(self):

        training_data_table_name="Customer Segmentation Test"
        columns=["ID","Gender","Ever_Married","Age","Graduated","Profession","Work_Experience","Spending_Score","Family_Size","Var_1","Segmentation"]
        resultant_column_name='Predicted_Cluster'
        resultant_table_name="Segmented Customer Data"
        import_type="truncateadd"

        # Path to the .pkl file
        pkl_file_path1 = self.ms.get_model_path('kmeans_model')
        pkl_file_path2 = self.ms.get_model_path('scaler')
        # Load the saved model and scaler
        kmeans = joblib.load(pkl_file_path1)
        scaler = joblib.load(pkl_file_path2)

        # Load new dataset or the same dataset for demonstration
        new_data : pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(training_data_table_name, columns,"")

        # Select features for k-means clustering (excluding ID and Segmentation)
        new_features = new_data.drop(columns=['ID', 'Segmentation'])

        # One-hot encoding for categorical variables
        new_features_encoded = pd.get_dummies(new_features, columns=['Gender', 'Ever_Married', 'Graduated', 'Profession', 'Var_1'])

        # Standardize the feature values using the loaded scaler
        new_features_scaled = scaler.transform(new_features_encoded)

        # Predict the clusters using the loaded model
        new_data[resultant_column_name] = kmeans.predict(new_features_scaled)

        output = pd.DataFrame({'ID': new_data.ID, resultant_column_name: new_data.Predicted_Cluster})
        output = output.astype({'ID': 'int64', resultant_column_name: 'int64'})  # Example casting, adjust as needed

        self.dt.upload_tabledata_from_DataFrame(resultant_table_name, output, {"importType": import_type})
