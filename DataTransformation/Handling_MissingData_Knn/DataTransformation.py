from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
from pandas import DataFrame
from sklearn.impute import KNNImputer


class DataTransformation:
    dt: DataTransformationUtil = None
    za: ZohoAnalytics = None

    def __init__(self, za):
        self.za = za
        self.dt = DataTransformationUtil(self.za)
        self.log = self.za.context.log

    def process_data(self):
        # Fetch the dataset from Zoho Analytics
        table_name="KnnData"
        column_names= ["Feature1", "Feature2", "Feature3", "Feature4"]
        final_table_name="KnnData_Processed"
        importtype="truncateadd"

        df: DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name,
                                                              column_names)

        # Log initial data
        self.log.INFO("Initial DataFrame fetched from Zoho Analytics:")
        self.log.INFO(df.head())

        # Initialize KNN Imputer with 5 neighbors
        imputer = KNNImputer(n_neighbors=5)

        # Apply KNN Imputation
        # Assuming all columns are numerical and need imputation
        df_imputed = DataFrame(imputer.fit_transform(df), columns=df.columns)

        # Log data after imputation
        self.log.INFO("DataFrame after KNN imputation:")
        self.log.INFO(df_imputed.head())

        # Upload the imputed dataset to Zoho Analytics
        self.dt.upload_tabledata_from_DataFrame(final_table_name, df_imputed, {"importType": importtype})

        # Log completion
        self.log.INFO("KNN imputation and upload completed successfully.")
