from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
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
        table_name="NoodleRating"
        column_names=["brand", "style", "rating"]
        final_table_name="NoodleRating_Duplicate_Removed"
        importType="truncateadd"

        # Fetch the table data from Zoho Analytics
        df = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)

        # Get the number of records in the original dataset
        num_records = df.shape[0]
        self.log.INFO(f"Number of records in the original dataset: {num_records}")

        # Drop duplicates, keeping the last occurrence based on 'brand' and 'style'
        df_cleaned = df.drop_duplicates(subset=['brand', 'style'], keep='last')

        # Get the number of records in the cleaned dataset
        num_records_cleaned = df_cleaned.shape[0]
        self.log.INFO(f"Number of records in the cl1eaned dataset: {num_records_cleaned}")

        # Print the cleaned DataFrame
        #self.log.INFO(f"Cleaned DataFrame:\n{df_cleaned}")

        # Upload the processed DataFrame back to Zoho Analytics
        self.dt.upload_tabledata_from_DataFrame(final_table_name, df_cleaned, {"importType": importType})

        # Log completion
        self.log.INFO("Data processing and upload completed")

