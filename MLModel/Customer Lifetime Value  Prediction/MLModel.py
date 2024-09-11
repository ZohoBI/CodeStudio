from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
from ModelStorage import ModelStorage
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
import xgboost as xgb
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
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

        training_data_table_name="CLV Train"
        columns=["Customer", "State", "Customer Lifetime Value", "Response", "Coverage", "Education", "Effective To Date",
            "EmploymentStatus", "Gender", "Income", "Location Code", "Marital Status", "Monthly Premium Auto",
            "Months Since Last Claim", "Months Since Policy Inception", "Number of Open Complaints", "Number of Policies",
            "Policy Type", "Policy", "Renew Offer Type", "Sales Channel", "Total Claim Amount", "Vehicle Class", "Vehicle Size"]
        target_column="Customer Lifetime Value"
        model_name='gbr_pipeline_model'
        directory = 'models'

        df: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(training_data_table_name, columns)
        # Handle missing data
        df.dropna(inplace=True)

        # Handle outliers
        clv_cap = df[target_column].quantile(0.99)
        income_cap = df['Income'].quantile(0.99)
        df[target_column] = np.clip(df[target_column], None, clv_cap)
        df['Income'] = np.clip(df['Income'], None, income_cap)

        # Feature engineering
        df['CLV_to_Income_Ratio'] = df[target_column] / df['Income']

        # Check and replace infinite values
        num_features = ['Monthly Premium Auto', 'Total Claim Amount', 'Income', 'CLV_to_Income_Ratio']
        df[num_features] = df[num_features].replace([np.inf, -np.inf], np.nan)

        # Drop rows with NaN values
        df.dropna(subset=num_features, inplace=True)

        # Train-test split
        train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

        # Scale numerical columns
        num_features = ['Monthly Premium Auto', 'Total Claim Amount', 'Income', 'CLV_to_Income_Ratio']

        # Encode categorical columns using One-Hot Encoding
        cat_cols = df.select_dtypes(include=['object']).columns
        cat_features = [col for col in cat_cols if col != 'Customer']

        # Create a preprocessor pipeline
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), num_features),
                ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), cat_features)  # Handle unknown categories
            ])

        # Train the model within a pipeline
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', GradientBoostingRegressor(random_state=42))
        ])

        # Fit the pipeline
        pipeline.fit(train_df, train_df[target_column])

        # Save the entire pipeline
        
        file_path = os.path.join(directory, model_name+'.pkl')
        os.makedirs(directory, exist_ok=True)
        joblib.dump(pipeline, file_path)
        self.ms.store_model(model_name, file_path)
        self.log.INFO(f"Pipeline model saved to {file_path}")


    def predict(self):

        training_data_table_name="CLV Test"
        columns=["Customer", "State", "Customer Lifetime Value", "Response", "Coverage", "Education", "Effective To Date",
            "EmploymentStatus", "Gender", "Income", "Location Code", "Marital Status", "Monthly Premium Auto",
            "Months Since Last Claim", "Months Since Policy Inception", "Number of Open Complaints", "Number of Policies",
            "Policy Type", "Policy", "Renew Offer Type", "Sales Channel", "Total Claim Amount", "Vehicle Class", "Vehicle Size"]
        target_column="Churn"
        model_name='gbr_pipeline_model'
        resultant_column_name='Predicted_Data'
        resultant_table_name="Predicted Customer Lifetime Value"
        import_type="truncateadd"

        # Load the saved pipeline model
        pkl_file_path = self.ms.get_model_path(model_name)
        pipeline = joblib.load(pkl_file_path)
    
        df: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(training_data_table_name, columns)
    
        # Handle outliers
        income_cap = df['Income'].quantile(0.99)
        df['Income'] = np.clip(df['Income'], None, income_cap)

        # Feature engineering
        df['CLV_to_Income_Ratio'] = df['Customer Lifetime Value'] / df['Income']

        # Check and replace infinite values
        num_features = ['Monthly Premium Auto', 'Total Claim Amount', 'Income', 'CLV_to_Income_Ratio']
        df[num_features] = df[num_features].replace([np.inf, -np.inf], np.nan)

        # Drop rows with NaN values
        df.dropna(subset=num_features, inplace=True)

        # Make predictions
        df[resultant_column_name] = pipeline.predict(df)

        # Prepare output DataFrame
        output = pd.DataFrame({'Customer': df['Customer'], resultant_column_name: df[resultant_column_name]})

        # Upload predictions
        self.dt.upload_tabledata_from_DataFrame(resultant_table_name, output, {"importType": import_type})
