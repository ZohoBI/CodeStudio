# Machine Maintenance Prediction Sample

## Overview

This code trains and saves a RandomForestClassifier to predict machine maintenance requirements based on historical data. It includes data transformation, model training, evaluation, and storage. Additionally, it supports making predictions on new data and uploading results for further analysis.

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

| Unique Identifier | Product ID | Type | Air Temperature | Process Temperature | Rotational Speed | Torque | Tool Wear | Machine Failure | Tool Wear Failure | Heat Dissipation Failure | Power Failure | Overstrain Failure | Random Failure |
|-------------------|------------|------|-----------------|---------------------|------------------|--------|-----------|-----------------|-------------------|--------------------------|---------------|---------------------|----------------|
| 848               | L48027     | L    | 296.4           | 307.4               | 2833             | 5.6    | 213       | 1               | 0                 | 0                        | 1             | 0                   | 0              |
| 1510              | L48689     | L    | 298.0           | 308.5               | 1429             | 37.7   | 220       | 1               | 1                 | 0                        | 0             | 0                   | 0              |
| 250               | L47429     | L    | 298.0           | 308.3               | 1405             | 56.2   | 218       | 1               | 0                 | 0                        | 0             | 1                   | 0              |
| 8927              | M23786     | M    | 297.3           | 308.3               | 1459             | 59.6   | 207       | 1               | 0                 | 0                        | 1             | 1                   | 0              |
| 1596              | L48775     | L    | 298.0           | 308.2               | 1365             | 52.9   | 218       | 1               | 0                 | 0                        | 0             | 1                   | 0              |


## Sample Output Data

| Unique Identifier | Product ID | Machine Maintenance  |
|-------------------|------------|----------------------|
| 9017              | L56196     | Maintenance Needed   |
| 1162              | L48341     | Maintenance Needed   |
| 8507              | L55686     | Maintenance Needed   |
| 904               | L48083     | Maintenance Needed   |
| 1497              | L48676     | Maintenance Needed   |
