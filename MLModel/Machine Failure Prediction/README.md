# Machine Failure Prediction
## Overview
This script predicts whether a machine may fail based on it's usage details.


1. Set the `table_name` variable to the name of the table that contains data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the `final_table_name` variable to the name of the table where the output data will be uploaded
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")

INPUT DATA:

| UDI | Product ID | Type | Air temperature [K] | Process temperature [K] | Rotational speed [rpm] | Torque [Nm] | Tool wear [min] | Target | Failure Type |
|-----|------------|------|---------------------|-------------------------|------------------------|-------------|-----------------|--------|--------------|
| 1   | M14860     | M    | 298.1               | 308.6                   | 1551                   | 42.8        | 0               | 0      | No Failure   |
| 2   | L47181     | L    | 298.2               | 308.7                   | 1408                   | 46.3        | 3               | 0      | No Failure   |
| 3   | L47182     | L    | 298.1               | 308.5                   | 1498                   | 49.4        | 5               | 0      | No Failure   |
| 4   | L47183     | L    | 298.2               | 308.6                   | 1433                   | 39.5        | 7               | 0      | No Failure   |


OUTPUT DATA:

| UDI  | Actual | Predicted |
|------|--------|-----------|
| 1604 | 0      | 0         |
| 8714 | 0      | 0         |
| 4562 | 0      | 0         |
| 6601 | 0      | 0         |
| 2559 | 0      | 0         |



