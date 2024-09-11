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