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

        sales_person_df = self.dt.fetch_tabledata_as_DataFrame("SalesPerson", ["Sales Person ID", "Sales Person Name", "Manager ID"])
        sales_df = self.dt.fetch_tabledata_as_DataFrame("SalesData", ["Sales ID", "Product Name", "Amount", "Sales Person ID"])

        merged_df = pd.merge(sales_df, sales_person_df, left_on='Sales Person ID', right_on='Sales Person ID')

        merged_df.rename({'Sales Person ID_x' : 'Sales Person ID'})
        manager_col_names = []
        def get_manager_names(id):
            manager_names = {}
            if pd.isnull(id):
                return manager_names
            manager_id = id
            level = 1
            while True:
                manager_row = sales_person_df.loc[sales_person_df['Sales Person ID'] == manager_id]
                if manager_row.empty:
                    break
                else:
                    manager_id = manager_row['Manager ID'].iloc[0]
                    manager_name = manager_row['Sales Person Name'].iloc[0]
                    manager_col_name = f'Manager {level} Name'
                    manager_names[manager_col_name] = manager_name
                    if manager_col_name not in manager_col_names:
                        manager_col_names.append(manager_col_name)
                    if pd.isnull(manager_id):
                        break
                    level += 1
            return manager_names

        manager_names_df = merged_df['Manager ID'].apply(lambda x: get_manager_names(x)).apply(pd.Series)
        merged_df = pd.concat([merged_df, manager_names_df], axis=1)

        def get_first_non_null(dfrow, columns_to_search):
            for c in columns_to_search:
                if pd.notnull(dfrow[c]):
                    return dfrow[c]
            return
        cols_to_search = manager_col_names[::-1]
        merged_df['Top Level Manager'] = merged_df.apply(lambda x: get_first_non_null(x, cols_to_search), axis=1)

        for col in list(merged_df.columns.values):
            if merged_df[col].dtype == 'object':
                merged_df[col] = merged_df[col].astype('string[python]')
        merged_df = merged_df[['Sales Person ID','Sales Person Name'] + manager_col_names + ['Top Level Manager', 'Amount']]
        self.dt.upload_tabledata_from_DataFrame("HierarchicalReporting", merged_df, {"importType": "truncateadd"})