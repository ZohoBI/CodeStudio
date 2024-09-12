from weakref import finalize

from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
from ModelStorage import ModelStorage
import joblib
import os
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
import math
from statsmodels.tsa.api import VAR
from scipy import stats


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
        table_name = "Revenue Data"
        column_names = ['Date', 'Amount', 'CROSS SELL', 'NEW',                                                                                 'REACTIVATE', 'RECURRING', 'REFUND',
                                                             'UPGRADE', 'OFFLINE', 'ONLINE',
                                                             'Direct', 'Reseller', 'ANZ', 'APAC',
                                                             'Antarctica',
                                                             'Brazil', 'Canada', 'China',
                                                             'ConEurope', 'India', 'India Central',
                                                             'India East', 'India North',
                                                             'India South',
                                                             'India West', 'Japan', 'LATAM', 'MEA',
                                                             'Others', 'UK', 'US', 'US Central',
                                                             'US East', 'US MST', 'US West']
        df: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)

        # self.log.INFO(df.shape)
        # self.log.INFO(df)
        # buffer = io.StringIO()
        # df.info(buf=buffer)
        # s = buffer.getvalue()
        # self.log.INFO(s)
        df['Date'] = pd.to_datetime(df['Date'])
        cols = ['Date', 'Amount']

        discrete_cols = []

        for col in df.columns:
            if col not in cols:
                discrete_cols.append(col)

        for i in discrete_cols:
            df[i] = df[i].replace(0, 1.0)

        discrete_cols.append('Amount')

        last_date = df['Date'].iloc[-1]

        df.set_index('Date', inplace=True)

        df = df[discrete_cols]
        # self.log.INFO(df.info())

        df = df.astype(float)

        # train = df[:-12]
        # test = df[-12:]

        # self.log.INFO(train.dtypes)
        model = VAR(df.diff()[1:])
        lag_order_results = model.select_order(maxlags=23)
        # print(lag_order_results.summary())

        forecast_weeks = 12

        optimal_lag = lag_order_results.selected_orders['aic']
        var_model = model.fit(optimal_lag)

        predicted = var_model.forecast(df.values[-optimal_lag:], steps=forecast_weeks)

        predicted_df = pd.DataFrame(predicted,
                                    index=pd.date_range(start=last_date + pd.Timedelta(weeks=1), periods=forecast_weeks,
                                                        freq='W-SUN'), columns=df.columns)

        # predicted_df = pd.DataFrame(predicted, index=test.index, columns=train.columns)
        # predicted_df['Actual_Amount'] = test['Amount']

        # print('Mean Squared Error (MSE):', mse)
        # print('Mean Absolute Error (MAE):', mae)
        # self.log.INFO(rmse)
        self.log.INFO(predicted_df)
        # self.log.INFO(test)
        # Save Trained Model
        directory = 'models'
        file_path = os.path.join(directory, 'forecast_var_model.pkl')
        os.makedirs(directory, exist_ok=True)
        joblib.dump(model, file_path)
        self.ms.store_model('forecast_var_model', file_path)
        self.ms.list_models()
        self.log.INFO("Training Completed...Procced to Predict")

    def predict(self):
        table_name = "Revenue Data"
        column_names = ['Date', 'Amount', 'CROSS SELL', 'NEW', 'REACTIVATE',
                                                             'RECURRING', 'REFUND', 'UPGRADE', 'OFFLINE', 'ONLINE',
                                                             'Direct', 'Reseller', 'ANZ', 'APAC', 'Antarctica',
                                                             'Brazil', 'Canada', 'China', 'ConEurope', 'India',
                                                             'India Central', 'India East', 'India North',
                                                             'India South', 'India West', 'Japan', 'LATAM', 'MEA',
                                                             'Others', 'UK', 'US', 'US Central', 'US East',
                                                             'US MST', 'US West']
        final_table_name = "ForecastedData"
        import_type = "truncateadd"
         # Path to the .pkl file
        pkl_file_path = self.ms.get_model_path('forecast_var_model')
        # Load the model from the .pkl file
        model = joblib.load(pkl_file_path)
        df: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)

        df['Date'] = pd.to_datetime(df['Date'])

        cols = ['Date', 'Amount']

        discrete_cols = []

        for col in df.columns:
            if col not in cols:
                discrete_cols.append(col)

        for i in discrete_cols:
            df[i] = df[i].replace(0, 1.0)

        last_date = df['Date'].iloc[-1]
        df.set_index('Date', inplace=True)
        df = df.astype(float)

        model = VAR(df.diff()[1:])
        lag_order_results = model.select_order(maxlags=23)
        # print(lag_order_results.summary())

        forecast_weeks = 8

        optimal_lag = lag_order_results.selected_orders['aic']
        var_model = model.fit(optimal_lag)

        predicted = var_model.forecast(df.values[-optimal_lag:], steps=forecast_weeks)

        predicted_df = pd.DataFrame(predicted,
                                    index=pd.date_range(start=last_date + pd.Timedelta(weeks=1), periods=forecast_weeks,
                                                        freq='W-SUN'), columns=df.columns)

        predicted_df = predicted_df.abs()
        predicted_df = predicted_df.reset_index(drop=False)
        # predicted_df.rename(columns = {'index': 'Date'}, inplace = True)

        self.log.INFO(predicted_df)
        # Now, 'model' contains the deserialized machine learning model
        # You can use the loaded model to make predictions or evaluate it
        # Example usage: Making predictions with the loaded model
        # Assuming you have test data in the variable 'X_test'
        self.dt.upload_tabledata_from_DataFrame(final_table_name, predicted_df, {"importType": import_type})