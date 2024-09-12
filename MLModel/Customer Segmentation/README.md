# Customer Segmentation Sample

## Overview

This code trains a KMeans clustering model to segment customers into distinct groups based on their attributes. It includes steps for data preprocessing, model training, and evaluation, as well as functionality for making predictions on new data. The model and scaler are saved and stored for future use, enabling improved customer targeting strategies.

Usage

1. Set the `training_data_table_name` variable to the name of the table in Zoho Analytics.
2. Set the `columns` variable to the list of column names to fetch from each table.
3. Set the `target_column` variable to the column you're trying to predict.
4. Set the `model_name` variable to the name you want to save your trained model as.
5. Set the `resultant_column_name` variable to the name you want to save the predicted column as. 
6. Set the `resultant_table_name` variable to the name of the table where the combined data will be uploaded.
7. Set the `import_type` variable to the import type for the upload (default: "truncateadd").
8. Set the `directory` variable to where you want save your trained model.

## Sample Input Data

| ID  | Gender | Ever Married | Age | Graduated | Profession | Work Experience | Spending Score | Family Size | Var_1 | Segmentation |
|-----|--------|--------------|-----|-----------|------------|-----------------|----------------|-------------|-------|--------------|
| 11  | 1      | 0            | 24  | 1         | 1          | 1               | 67             | 3           | 2     | 1            |
| 77  | 1      | 1            | 16  | 0         | 5          | 3               | 59             | 5           | 3     | 1            |
| 78  | 0      | 0            | 25  | 1         | 1          | 1               | 54             | 5           | 3     | 1            |
| 101 | 1      | 0            | 22  | 0         | 1          | 2               | 55             | 6           | 3     | 1            |
| 250 | 1      | 0            | 20  | 1         | 2          | 1               | 55             | 4           | 1     | 1            |

## Sample Output Data

| ID  | Predicted Cluster |
|-----|-------------------|
| 11  | 2                 |
| 77  | 0                 |
| 78  | 3                 |
| 101 | 2                 |
| 250 | 1                 |