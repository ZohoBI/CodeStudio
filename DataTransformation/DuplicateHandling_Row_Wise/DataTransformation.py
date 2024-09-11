from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
from pandas import DataFrame


class DataTransformation:
    dt: DataTransformationUtil = None
    za: ZohoAnalytics = None

    def __init__(self, za):
        self.za = za
        self.dt = DataTransformationUtil(self.za)
        self.log = self.za.context.log

    def process_data(self):
        table_name = "sales_duplicate"
        column_names = ["OrderID", "ProductID", "Quantity", "Price", "Date"]
        final_table_name = "sales_data_duplicateremoved"
        importType = "truncateadd"

        df: DataFrame = self.dt.fetch_tabledata_as_DataFrame(
            table_name,
            column_names
        )

        # Remove duplicate rows
        df_unique: DataFrame = df.drop_duplicates()

        df_unique = df_unique.astype(str)

        self.dt.upload_tabledata_from_DataFrame(final_table_name, df_unique, {"importType": importType})

        self.log.INFO("Duplicate data removed");
