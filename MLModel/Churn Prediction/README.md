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

## Sample Input Data : 

| ID | Tenure | WarehouseToHome | NumberOfDeviceRegistered | PreferedOrderCat    | SatisfactionScore | MaritalStatus | NumberOfAddress | Complain | DaySinceLastOrder | CashbackAmount | Churn |
|----|--------|------------------|--------------------------|---------------------|-------------------|---------------|-----------------|----------|-------------------|----------------|-------|
| 1  | 15     | 29               | 4                        | Laptop & Accessory  | 3                 | Single        | 2               | 0        | 7                 | 143.32         | 0     |
| 2  | 7      | 25               | 4                        | Mobile              | 1                 | Married       | 2               | 0        | 7                 | 129.29         | 0     |
| 3  | 27     | 13               | 3                        | Laptop & Accessory  | 1                 | Married       | 5               | 0        | 7                 | 168.54         | 0     |
| 4  | 20     | 25               | 4                        | Fashion             | 3                 | Divorced      | 7               | 0        | 3                 | 230.27         | 0     |
| 5  | 30     | 15               | 4                        | Others              | 4                 | Single        | 8               | 0        | 8                 | 322.17         | 0     |

## Sample Output Data

| ID | Prediction |
|----|------------|
| 1  | 0          |
| 5  | 0          |
| 9  | 0          |
| 13 | 0          |
| 17 | 0          |