# Churn Prediction Sample

## Overview

This code trains an XGBoost classifier to predict customer churn using historical data, with preprocessing steps for handling categorical variables and missing values. It evaluates the model's performance with classification metrics and saves the trained model for future predictions. The model helps in identifying at-risk customers, enabling more effective retention strategies.

Usage

1. Set the `training_data_table_name` variable to the name of the table in Zoho Analytics.
2. Set the `columns` variable to the list of column names to fetch from each table.
3. Set the `target_column` variable to the column you're trying to predict.
4. Set the `model_name` variable to the name you want to save your trained model as.
5. Set the `resultant_column_name` variable to the name you want to save the predicted column as. 
6. Set the `resultant_table_name` variable to the name of the table where the combined data will be uploaded.
7. Set the `import_type` variable to the import type for the upload (default: "truncateadd").