import pandas as pd
from pandas import DataFrame
from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics


class DataTransformation:
    dt: DataTransformationUtil = None
    za: ZohoAnalytics = None

    def __init__(self, za):
        self.za = za
        self.dt = DataTransformationUtil(self.za)
        self.log = self.za.context.log

    def int_to_binary_str(self, n, bits=3):
        """Convert an integer to a binary string with a fixed number of bits."""
        return format(n, f'0{bits}b')

    def process_data(self):
        table_name = "Customer_Feedback"
        column_names = ["ID", "Feedback Sentiment"]
        final_table_name = "Binary Encoding"
        importType = "truncateadd"

        # Fetch table data as DataFrame
        df: DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)

        # Define the categories and their integer mappings
        categories = ['Positive', 'Neutral', 'Negative', 'Very Positive', 'Very Negative', 'Mixed']
        category_to_int = {cat: i for i, cat in enumerate(categories)}

        # Log the category-to-integer mapping
        self.log.INFO(f"{category_to_int}")

        # Convert feedback sentiments to integers
        df['Feedback Integer'] = df['Feedback Sentiment'].map(category_to_int)

        # Apply binary encoding using self.int_to_binary_str
        df['Binary'] = df['Feedback Integer'].apply(lambda x: self.int_to_binary_str(x, bits=3))

        # Split the binary encoding into separate columns
        df[['Bit1', 'Bit2', 'Bit3']] = df['Binary'].apply(lambda x: pd.Series(list(x))).astype(int)

        # Drop intermediate columns
        df = df.drop(columns=['Feedback Integer', 'Binary'])

        # Upload transformed data
        self.dt.upload_tabledata_from_DataFrame(final_table_name, df, {"importType": importType})
        self.log.INFO("Upload Completed")
