from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
from pandas import DataFrame
from scipy import stats


class DataTransformation:
    dt: DataTransformationUtil = None
    za: ZohoAnalytics = None

    def __init__(self, za):
        self.za = za
        self.dt = DataTransformationUtil(self.za)
        self.log = self.za.context.log

    def detect_outliers_zscore(self, df: DataFrame, column: str, threshold: float = 2) -> (DataFrame, DataFrame):
        # Calculate Z-scores
        z_scores = stats.zscore(df[column])

        # Identify higher and lower outliers
        higher_outliers = df[z_scores > threshold].copy()
        lower_outliers = df[z_scores < -threshold].copy()

        # Debug: print sample Z-scores and number of outliers detected
        self.log.INFO(f"Sample Z-scores: {z_scores[:5]}")
        self.log.INFO(f"Number of higher outliers: {len(higher_outliers)}")
        self.log.INFO(f"Number of lower outliers: {len(lower_outliers)}")

        return higher_outliers, lower_outliers

    def process_data(self):
        table_name = "SAMPLE_SALES"
        column_names = ["ID", "Sales"]
        final_table_name_1 = "HigherOutliers"
        final_table_name_2 = "LowerOutliers"
        importType = "truncateadd"

        # Fetch data from Zoho Analytics
        df: DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)

        # Detect outliers using Z-Score method
        higher_outliers, lower_outliers = self.detect_outliers_zscore(df, 'Sales', 2)

        # Upload higher outliers to Zoho Analytics
        if not higher_outliers.empty:
            self.dt.upload_tabledata_from_DataFrame(final_table_name_1, higher_outliers, {"importType": importType})
            self.log.INFO("Higher outliers uploaded to Zoho Analytics")
        else:
            self.log.INFO("No higher outliers to upload")

        # Upload lower outliers to Zoho Analytics
        if not lower_outliers.empty:
            self.dt.upload_tabledata_from_DataFrame(final_table_name_2, lower_outliers, {"importType": importType})
            self.log.INFO("Lower outliers uploaded to Zoho Analytics")
        else:
            self.log.INFO("No lower outliers to upload")
        # Log completion message
        self.log.INFO("Outlier detection and upload completed")
