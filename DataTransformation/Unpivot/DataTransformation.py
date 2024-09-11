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
        table_name="Perfomance_review"
        column_names=["Employee", "Quarter", "Sales", "Marketing", "Development", "Support"]
        final_table_name="employee_performance_reviews_unpivoted"
        importType="truncateadd"

        # Fetch the data from Zoho Analytics table "employee_performance_reviews"
        df: DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)
        
        # Unpivot the DataFrame
        unpivoted_df: DataFrame = df.melt(id_vars=['Employee', 'Quarter'],
                                         value_vars=['Sales', 'Marketing', 'Development', 'Support'],
                                         var_name='Metric',
                                         value_name='Rating')

        # Convert all columns to string if necessary
        unpivoted_df = unpivoted_df.astype(str)
        
        # Save the unpivoted DataFrame to a new table in Zoho Analytics
        self.dt.upload_tabledata_from_DataFrame(final_table_name, unpivoted_df, {"importType": importType})
        
        self.log.INFO("Unpivoting completed")


