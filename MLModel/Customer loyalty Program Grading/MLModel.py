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
                # Update with the loyalty program data
        training_data_table_name = "Flight Loyalty Flight Train"
        columns = ["Distance", "Dollar Cost Points Redeemed", "Flights Booked", "Flights with Companions", "Loyalty Number", 
                   "Month", "Points Accumulated", "Points Redeemed", "Total Flights", "Year"]
        resultant_column_name = 'Predicted_Cluster'

        # Fetch the data
        df: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(training_data_table_name, columns, "")

        # Drop irrelevant columns for clustering
        features = df.drop(columns=['Loyalty Number', 'Month', 'Year'])  # Exclude non-numeric columns

        # Handle missing values (if any)
        features = features.fillna(0)  # Replace NaNs with 0 or use other imputation strategies

        # Standardize the feature values
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)

        # Train k-means clustering model
        kmeans = KMeans(n_clusters=4, random_state=42)
        kmeans.fit(features_scaled)

        # Predict the clusters
        df[resultant_column_name] = kmeans.predict(features_scaled)

        # Prepare output
        output = pd.DataFrame({'Loyalty Number': df['Loyalty Number'], resultant_column_name: df[resultant_column_name]})
        self.log.INFO(output)

        # Save the model and scaler
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
        self.log.INFO("Training Completed...Proceed to Predict")

    def predict(self):
        # Update with the loyalty program data
        training_data_table_name = "Flight Loyalty Flight Test"
        columns = [
            "Distance", "Dollar Cost Points Redeemed", "Flights Booked", "Flights with Companions", "Loyalty Number", 
            "Month", "Points Accumulated", "Points Redeemed", "Total Flights", "Year"
            ]
        resultant_column_name = 'Predicted_Cluster'
        resultant_table_name = "Classified Loyalty Program Customers"
        import_type = "truncateadd"
        n_clusters = 4
    
        # Path to the .pkl file
        pkl_file_path1 = self.ms.get_model_path('kmeans_model')
        pkl_file_path2 = self.ms.get_model_path('scaler')
    
        # Load the saved model and scaler
        kmeans = joblib.load(pkl_file_path1)
        scaler = joblib.load(pkl_file_path2)

        # Load new dataset
        new_data: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(training_data_table_name, columns, "")

        # Drop irrelevant columns for clustering
        new_features = new_data.drop(columns=['Loyalty Number', 'Month', 'Year'])

        # Handle missing values (if any)
        new_features = new_features.fillna(0)

        # Standardize the feature values using the loaded scaler
        new_features_scaled = scaler.transform(new_features)

        # Predict the clusters using the loaded model
        new_data[resultant_column_name] = kmeans.predict(new_features_scaled)

        # Assign Cluster Labels (if needed)
        new_data['Cluster_Label'] = [
            'Grade ' + str(n_clusters - pred) for pred in new_data[resultant_column_name]
        ]

        # Prepare output
        output = pd.DataFrame({
            'Loyalty Number': new_data['Loyalty Number'],
            resultant_column_name: new_data[resultant_column_name],
            'Cluster_Label': new_data['Cluster_Label']
        })

        output['Loyalty Number'] = output['Loyalty Number'].astype('float')
        output[resultant_column_name] = output[resultant_column_name].astype('float')
        output['Cluster_Label'] = output['Cluster_Label'].astype('string')

        # Upload the segmented data
        self.dt.upload_tabledata_from_DataFrame(resultant_table_name, output, {"importType": import_type})

        self.log.INFO("Prediction completed and data uploaded.")
