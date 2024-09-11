# Customer Lifetime Value Prediction Sample

## Overview

This code trains a Gradient Boosting Regressor to predict Customer Lifetime Value (CLV) using a pipeline that includes data preprocessing and feature engineering. It handles missing values and outliers, then evaluates and saves the model for future predictions. The model is used to predict CLV for new data, aiding in more targeted customer strategies.

Usage

1. Set the `training_data_table_name` variable to the name of the table in Zoho Analytics.
2. Set the `columns` variable to the list of column names to fetch from each table.
3. Set the `target_column` variable to the column you're trying to predict.
4. Set the `resultant_column_name` variable to the name you want to save the predicted column as. 
5. Set the `resultant_table_name` variable to the name of the table where the combined data will be uploaded.
6. Set the `import_type` variable to the import type for the upload (default: "truncateadd").