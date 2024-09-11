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
        table_name = "Event_data"
        column_names = ["Event_ID", "DateTime"]
        final_table_name = "Event_Data_Extracted"
        importType = "truncateadd"

        df: DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)

        # Convert the DateTime column to datetime objects
        df['DateTime'] = pd.to_datetime(df['DateTime'])

        # Extract features from DateTime
        df['Year'] = df['DateTime'].dt.year.astype('int64')
        df['Month'] = df['DateTime'].dt.month.astype('int64')
        df['Day'] = df['DateTime'].dt.day.astype('int64')
        df['Hour'] = df['DateTime'].dt.hour.astype('int64')
        df['DayOfWeek'] = df['DateTime'].dt.dayofweek.astype('int64')  # Monday=0, Sunday=6

        # Upload transformed data
        self.dt.upload_tabledata_from_DataFrame(final_table_name, df, {"importType": importType});




