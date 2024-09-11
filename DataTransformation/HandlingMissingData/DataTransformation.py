from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
from pandas import DataFrame
import numpy as np

class DataTransformation:
    dt: DataTransformationUtil = None
    za: ZohoAnalytics = None

    def __init__(self, za):
        self.za = za
        self.dt = DataTransformationUtil(self.za)
        self.log = self.za.context.log

    def process_data(self):
        table_name="EmployeeData"
        column_names=["ID", "Name", "Department", "Salary", "Age"]
        final_table_name_1="EmployeeDataMeanProcessed"
        final_table_name_2="EmployeeDataMedianProcessed"
        final_table_name_3="EmployeeDataModeProcessed"
        final_table_name_4="EmployeeDataDroppedProcessed"
        importType="truncateadd"


        # Fetch data from Zoho Analytics
        df: DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)
        
        # Process data with mean, median, mode and dropping missing values
        df_mean_filled: DataFrame = self.fill_missing_with_mean(df)
        df_median_filled: DataFrame = self.fill_missing_with_median(df)
        df_mode_filled: DataFrame = self.fill_missing_with_mode(df)
        df_dropped: DataFrame = self.drop_missing_values(df)

        # Upload processed data to Zoho Analytics
        self.upload_to_workspace(final_table_name_1, df_mean_filled)
        self.upload_to_workspace(final_table_name_2, df_median_filled)
        self.upload_to_workspace(final_table_name_3, df_mode_filled)
        self.upload_to_workspace(final_table_name_4, df_dropped)

        self.log.INFO("Data processing completed and uploaded.")

    def fill_missing_with_mean(self, df: DataFrame) -> DataFrame:
        df_filled = df.copy()
        df_filled['Age'].fillna(df_filled['Age'].mean(), inplace=True)
        return df_filled

    def fill_missing_with_median(self, df: DataFrame) -> DataFrame:
        df_filled = df.copy()
        df_filled['Age'].fillna(df_filled['Age'].median(), inplace=True)
        return df_filled

    def fill_missing_with_mode(self, df: DataFrame) -> DataFrame:
        df_filled = df.copy()
        mode_value = df_filled['Age'].mode().iloc[0]
        df_filled['Age'].fillna(mode_value, inplace=True)
        return df_filled

    def drop_missing_values(self, df: DataFrame) -> DataFrame:
        df_dropped = df.dropna()
        return df_dropped

    def upload_to_workspace(self, table_name: str, df: DataFrame):
        self.dt.upload_tabledata_from_DataFrame(table_name, df, {"importType": importType})
        self.log.INFO(f"{table_name} uploaded successfully.")