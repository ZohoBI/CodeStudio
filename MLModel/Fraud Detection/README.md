# Fraud Detection Sample

## Overview

This code trains a RandomForestClassifier to detect fraudulent transactions using a preprocessed dataset. It includes steps for data transformation, model training, and evaluation, as well as functionality for making predictions on new data and uploading results. The model is saved and stored for future use.

Usage

1. Set the `training_data_table_name` variable to the name of the table in Zoho Analytics.
2. Set the `columns` variable to the list of column names to fetch from each table.
3. Set the `target_column` variable to the column you're trying to predict.
4. Set the `model_name` variable to the name you want to save your trained model as.
5. Set the `resultant_column_name` variable to the name you want to save the predicted column as. 
6. Set the `resultant_table_name` variable to the name of the table where the combined data will be uploaded
7. Set the `import_type` variable to the import type for the upload (default: "truncateadd")
8. Set the `directory` variable to where you want save your trained model.

## Sample Input Data

| ID   | trans_date_trans_time   | cc_num         | merchant                              | category       | amt  | first   | last    | gender | street                            | city      | state | zip   | lat    | long    | city_pop | job                      | dob         | trans_num                          | unix_time | merch_lat | merch_long | is_fraud | age         |
|------|--------------------------|-----------------|--------------------------------------|----------------|------|---------|---------|--------|-----------------------------------|-----------|-------|-------|--------|---------|----------|--------------------------|-------------|-------------------------------------|-----------|-----------|------------|----------|------------|
| 120  | 01/01/2019 01:31         | 4.64289E+12     | fraud_Wuckert-Walter                  | grocery_net    | 38.7 | Eddie   | Mendez  | M      | 1831 Faith View Suite 653        | Clarinda  | IA    | 51632 | 40.7491| -95.038 | 7297     | IT trainer              | 13/07/1990  | 83afa07b375903bed0eef11840145895     | 1325381502| 39.880088 | -94.193907 | 0        | 28.49041096|
| 121  | 01/01/2019 01:31         | 5.01883E+11     | fraud_Weber and Sons                  | food_dining    | 98.24| Melissa | Phillips| F      | 5069 Scott Pass Apt. 654          | Meadville | MS    | 39653 | 31.4285| -90.8578| 2799     | Therapist, horticultural | 21/01/1961  | 6658882e9274e3d6fc3dffa5593b8ad6     | 1325381513| 30.906565 | -90.486622 | 0        | 57.98356164|
| 3168 | 02/01/2019 17:49         | 4.60707E+15     | fraud_Romaguera, Cruickshank and Greenholt | shopping_net   | 3.85 | Brenda  | Perez   | F      | 033 Tara Brook Suite 523          | Coyle     | OK    | 73027 | 35.8985| -97.2607| 1493     | Amenity horticulturist   | 21/03/1985  | 7c2cdc5b1850a96ff82ace793666ecbc     | 1325526588| 36.554124 | -97.999695 | 0        | 33.80821918|
| 3169 | 02/01/2019 17:51         | 4.15895E+15     | fraud_Romaguera, Wehner and Tromp     | kids_pets      | 48.23| Justin  | Bell    | M      | 5323 Walker Island                | Pittsburgh| PA    | 15217 | 40.4308| -79.9205| 687276   | Scientist, marine         | 19/10/1973  | e785ab39a2ef72e671bed753f4f036ab     | 1325526675| 40.567948 | -79.674151 | 0        | 45.23561644|
| 3170 | 02/01/2019 17:52         | 3.50238E+15     | fraud_Torphy-Kertzmann                | health_fitness | 6.3  | Kathleen| Martin  | F      | 659 Nicole Cove Suite 560          | New Waverly| TX    | 77358 | 30.5354| -95.4532| 4993     | Scientist, biomedical      | 30/11/1948  | 7dec3921921e15e8fcb02495132669db     | 1325526766| 30.349795 | -95.717806 | 0        | 70.1369863 |


## Sample Output Data

| ID  | Predicted Cluster |
|-----|-------------------|
| 11  | 2                 |
| 77  | 0                 |
| 78  | 3                 |
| 101 | 2                 |
| 250 | 1                 |
