from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
from pandas import DataFrame
from sklearn.preprocessing import LabelEncoder


class DataTransformation:
    dt: DataTransformationUtil = None
    za: ZohoAnalytics = None

    def __init__(self, za):
        self.za = za
        self.dt = DataTransformationUtil(self.za)
        self.log = self.za.context.log

    def process_data(self):
        table_name = "Fruit_Data"
        column_names = ["Fruit", "Color", "Price"]
        final_table_name = "Label_Encoding"
        importType = "truncateadd"

        df: DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)

        # Initialize LabelEncoders for 'Fruit'
        fruit_encoder = LabelEncoder()
        fruit_encoded = fruit_encoder.fit_transform(df['Fruit'])
        df['Fruit_Encoded'] = fruit_encoded

        self.log.INFO(f"{df.head()}")
        self.dt.upload_tabledata_from_DataFrame(final_table_name, df, {"importType": importType})
        self.log.INFO("Upload Completed")



