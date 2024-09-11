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
        table_name = "SalesData"
        column_names = ["Date", "Region", "Product Category", "Sales"]
        final_table_name_1 = "WestRegionSales"
        final_table_name_2 = "StationerySales"
        final_table_name_3 = "HighSales"
        final_table_name_4 = "Subset data"
        final_table_name_5 = "Sales_In_West"
        importType = "truncateadd"
        sales = 'Sales'

        # Fetch data from "StoreSales" table
        df: DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)

        # Log the DataFrame to verify data
        self.log.INFO(f"Fetched DataFrame:\n{df.head()}")

        # Data Cleaning
        df[sales] = df[sales].replace({'\$': '', ',': ''}, regex=True).astype(float)

        # Filter by region
        west_region_sales = df[df['Region'] == 'West']

        # Filter by product category
        stationery_sales = df[df['Product Category'] == 'Stationery']

        # Filter by sales amount greater than $1,000
        high_sales = df[df[sales] > 1000]

        # subset columns
        subset_columns = df[['Date', 'Region', sales]]

        sales_in_west = df[(df[sales] < 1000) & (df['Product Category'] == 'Stationery') & (df['Region'] == 'West')]

        # Log filtered data
        self.log.INFO(f"Combined data:\n{sales_in_west.head()}")
        self.log.INFO(f"West Region Sales:\n{west_region_sales.head()}")
        self.log.INFO(f"Stationery Sales:\n{stationery_sales.head()}")
        self.log.INFO(f"High Sales:\n{high_sales.head()}")
        self.log.INFO(f"Subset Columns:\n{subset_columns.head()}")

        # Upload the filtered data back to Zoho Analytics
        self.dt.upload_tabledata_from_DataFrame(final_table_name_1, west_region_sales, {"importType": importType})
        self.dt.upload_tabledata_from_DataFrame(final_table_name_2, stationery_sales, {"importType": importType})
        self.dt.upload_tabledata_from_DataFrame(final_table_name_3, high_sales, {"importType": importType})
        self.dt.upload_tabledata_from_DataFrame(final_table_name_4, subset_columns, {"importType": importType})
        self.dt.upload_tabledata_from_DataFrame(final_table_name_5, sales_in_west, {"importType": importType})
        # Log completion message
        self.log.INFO("Data filtering and subsetting completed and uploaded.")


