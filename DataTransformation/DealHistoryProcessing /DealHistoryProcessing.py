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
        history_table = "Deal History"
        output_table = "Deal History Processed"
        df: DataFrame = self.dt.fetch_tabledata_as_DataFrame(history_table, ["Id", "Deal Id", "Stage","Modified Time"])
        df['Modified Time'] = pd.to_datetime(df['Modified Time'])
        df = df.sort_values(by=['Deal Id', 'Modified Time'])
        df['Next Stage'] = df.groupby('Deal Id')['Stage'].shift(-1)
        df['Prev Stage'] = df.groupby('Deal Id')['Stage'].shift(1)
        self.dt.upload_tabledata_from_DataFrame(output_table, df, {"importType": "truncateadd"})

