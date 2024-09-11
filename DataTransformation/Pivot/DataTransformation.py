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
        tablename = "StoreSales"
        column_names = ["Region", "Product Category", "Sales"]
        final_table_name="Pivoted_SalesData"
        importType = "truncateadd"

        # Fetch data from Zoho Analytics and create DataFrame
        df: DataFrame = self.dt.fetch_tabledata_as_DataFrame(tablename, column_names)

        # Pivot table to get separate columns for each product category dynamically
        pivot_df: DataFrame = df.pivot_table(index='Region', columns='Product Category', values='Sales', aggfunc='sum', fill_value=0)

        # Calculate Total Sales
        pivot_df['TotalSales'] = pivot_df.sum(axis=1)

        # Reset index to make 'Region' a column
        pivot_df = pivot_df.reset_index()

        # Upload processed DataFrame to Zoho Analytics
        self.dt.upload_tabledata_from_DataFrame(final_table_name, pivot_df, {"importType": importType})

        # Log completion message
        self.log.INFO("Data transformation and upload to Pivoted_SalesData completed")
