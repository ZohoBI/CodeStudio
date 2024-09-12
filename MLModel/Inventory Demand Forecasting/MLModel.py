from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
from ModelStorage import ModelStorage
import pandas as pd
import numpy as np
from datetime import datetime, date
#need to import library
import holidays
import calendar
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import r2_score
import joblib
import os


class MLModel:
    dt: DataTransformationUtil = None
    za: ZohoAnalytics = None
    ms: ModelStorage = None

    def __init__(self, za, ms):
        self.za = za
        self.dt = DataTransformationUtil(self.za)
        self.log = self.za.context.log
        self.ms = ms

    def fit(self):
        table_name = "Inventory Demand Train Data"
        column_names =   ["date", "store", "item", "sales"]
        df: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)

        df['date'] = pd.to_datetime(df['date'])

        def create_date_features(df):
            df["month"] = df.date.dt.month
            df["day_of_month"] = df.date.dt.day
            df["day_of_year"] = df.date.dt.dayofyear
            df["week_of_year"] = df.date.dt.isocalendar().week.astype(int)
            df["day_of_week"] = df.date.dt.dayofweek
            df["year"] = df.date.dt.year
            df["is_wknd"] = df.date.dt.weekday // 4
            df['is_holiday'] = df.date.isin(holidays.IN()) * 1
            df["is_month_start"] = df.date.dt.is_month_start.astype(int)
            df["is_month_end"] = df.date.dt.is_month_end.astype(int)
            return df

        df = create_date_features(df)

        # adding cyclical features
        df['m1'] = np.sin(df['month'] * (2 * np.pi / 12))
        df['m2'] = np.cos(df['month'] * (2 * np.pi / 12))

        train = df.loc[(df["date"] < "2017-01-01"), :]
        test = df.loc[(df["date"] >= "2017-01-01") & (df["date"] < "2017-04-01"), :]

        date_col = test['date']

        X_train = train.drop(['date', 'sales'], axis=1)
        y_train = train['sales']
        X_test = test.drop(['date', 'sales'], axis=1)
        y_test = test['sales']

        model_xgb = XGBRegressor()
        model_xgb.fit(X_train, y_train)
        y_pred_xgb = model_xgb.predict(X_test)

        self.log.INFO(mae(y_test, y_pred_xgb))
        # print("mse: ", mse(y_test, y_pred_xgb))
        self.log.INFO(np.sqrt(mse(y_test, y_pred_xgb)))
        # print("r2_score: ", r2_score(y_test, y_pred_xgb))
        # print("mape: ", np.mean(np.abs((y_test - y_pred_xgb)/ y_test)) * 100)

        output = pd.DataFrame({'Forecasted Demand': y_pred_xgb})
        output['Forecasted Demand'] = np.round(output['Forecasted Demand'], 2)
        # print(output.info())

        X_test.reset_index(drop=True, inplace=True)
        y_test.reset_index(drop=True, inplace=True)

        X_test_cols = X_test[['store', 'item', 'month', 'day_of_month', 'day_of_year', 'day_of_week', 'year', 'is_wknd',
                              'is_month_start', 'is_month_end']]
        X_test_cols.head()

        output = pd.concat([date_col, output, y_test, X_test_cols], axis=1)

        self.log.INFO(output)
        # Save Trained Model
        directory = 'models'
        file_path = os.path.join(directory, 'XGBRegressorIVDemand.pkl')
        os.makedirs(directory, exist_ok=True)
        joblib.dump(model_xgb, file_path)
        self.ms.store_model('XGBRegressorIVDemand', file_path)
        self.ms.list_models()
        self.log.INFO("Training Completed...Procced to Predict")

    def predict(self):
        table_name = "Inventory Demand Validation Data"
        column_names =  ["id", "date", "store", "item"]
        final_table_name = "Forecasted Inventory Demand Data"
        import_type = "truncateadd"
        # Path to the .pkl file
        pkl_file_path = self.ms.get_model_path('XGBRegressorIVDemand')
        # Load the model from the .pkl file
        model = joblib.load(pkl_file_path)

        df: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)


        df['date'] = pd.to_datetime(df['date'])

        def create_date_features(df):
            df["month"] = df.date.dt.month
            df["day_of_month"] = df.date.dt.day
            df["day_of_year"] = df.date.dt.dayofyear
            df["week_of_year"] = df.date.dt.isocalendar().week.astype(int)
            df["day_of_week"] = df.date.dt.dayofweek
            df["year"] = df.date.dt.year
            df["is_wknd"] = df.date.dt.weekday // 4
            df["is_month_start"] = df.date.dt.is_month_start.astype(int)
            df["is_month_end"] = df.date.dt.is_month_end.astype(int)
            return df

        df = create_date_features(df)

        # adding cyclical features
        df['m1'] = np.sin(df['month'] * (2 * np.pi / 12))
        df['m2'] = np.cos(df['month'] * (2 * np.pi / 12))

        X = df.drop(['id', 'date'], axis=1)

        preds = model.predict(X)

        output = pd.DataFrame({'Forecasted Demand': preds})
        output['Forecasted Demand'] = np.round(output['Forecasted Demand'], 0)

        df.reset_index(drop=True, inplace=True)

        X_cols = df[['id', 'date', 'store', 'item', 'month']]

        output = pd.concat([X_cols, output], axis=1)

        self.log.INFO(output)

        output[['id', 'store', 'item', 'month', 'Forecasted Demand']] = output[
            ['id', 'store', 'item', 'month', 'Forecasted Demand']].astype('float')

        self.dt.upload_tabledata_from_DataFrame(final_table_name, output,
                                                {"importType": import_type})