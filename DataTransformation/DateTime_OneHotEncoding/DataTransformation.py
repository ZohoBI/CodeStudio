from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
from pandas import DataFrame
import pandas as pd


class DataTransformation:
    dt: DataTransformationUtil = None
    za: ZohoAnalytics = None

    def __init__(self, za):
        self.za = za
        self.dt = DataTransformationUtil(self.za)
        self.log = self.za.context.log

    def process_data(self):
        table_name = "Event_Data"
        column_names = ["Event_ID", "DateTime"]
        final_table_name = "Event_Data_ONEHOT_ENCODING"
        importType = "truncateadd"

        df: DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)

        # Step 2: Convert the 'DateTime' column to datetime objects
        df['DateTime'] = pd.to_datetime(df['DateTime'])

        # Step 3: Extract the month from the 'DateTime' column
        df['Month'] = df['DateTime'].dt.month

        # Step 4: Apply one-hot encoding to the 'Month' column
        df_encoded = pd.get_dummies(df, columns=['Month'], prefix='Month')

        for column in df_encoded.columns:
            if df_encoded[column].dtype == bool:
                df_encoded[column] = df_encoded[column].astype(int)

        # Upload transformed data
        self.dt.upload_tabledata_from_DataFrame(final_table_name, df_encoded, {"importType": importType});




