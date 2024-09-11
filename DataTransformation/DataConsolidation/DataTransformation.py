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
        # Define the tables to consolidate
        table_names = ['Sales_data_Inr', 'Sales_data_Usd', 'Sales_data_Euro', 'Sales_data_JPY']
        column_names = ["ID", "SALES"]
        final_table_name = "combined_sales_data"
        import_type = "truncateadd"

        dataframes= []

        for table_name in table_names:
            # Fetch data from Zoho Analytics table
            df : DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)
            dataframes.append(df)

        concat_frame : DataFrame = pd.concat(dataframes)

        # Upload processed data back to Zoho Analytics
        self.dt.upload_tabledata_from_DataFrame(final_table_name, concat_frame, {"importType": import_type})
        self.log.INFO("Data processing and upload completed successfully.")
