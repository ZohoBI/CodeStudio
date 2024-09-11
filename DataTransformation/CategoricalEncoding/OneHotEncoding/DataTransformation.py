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
        table_name = "Customer_Purchase"
        column_names = ["CustomerID", "Gender", "Age", "ProductCategory", "AmountSpent"]
        final_table_name = "OneHotEncoded"
        importType = "truncateadd"

        df: DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)

        df_encoded: DataFrame = pd.get_dummies(df, columns=['Gender', 'ProductCategory'])

        df_encoded = df_encoded.astype(int)

        self.dt.upload_tabledata_from_DataFrame(final_table_name, df_encoded, {"importType": importType});

        self.log.INFO("Uploaded")