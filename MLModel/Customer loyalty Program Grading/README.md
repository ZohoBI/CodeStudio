# Customer Loyalty Program Grading Sample

## Overview

The code trains a K-Means clustering model to classify customers in a loyalty program into distinct grades based on their behavior. It processes and standardizes data, trains the model, and saves both the model and scaler for future use. The class also predicts customer clusters for new data, assigning grades for differentiated rewards, and manages data transformations and model storage efficiently.

Usage

1. Set the `training_data_table_name` variable to the name of the table in Zoho Analytics.
2. Set the `columns` variable to the list of column names to fetch from each table.
5. Set the `resultant_column_name` variable to the name you want to save the predicted column as. 
6. Set the `resultant_table_name` variable to the name of the table where the combined data will be uploaded.
7. Set the `import_type` variable to the import type for the upload (default: "truncateadd").
8. Set the `n_clusters` variable to how many clusters you want.

## Sample Input Data 1

| Loyalty Number | Year | Month | Flights Booked | Flights with Companions | Total Flights | Distance | Points Accumulated | Points Redeemed | Dollar Cost Points Redeemed |
|----------------|------|-------|----------------|-------------------------|---------------|----------|---------------------|-----------------|------------------------------|
| 117408         | 2017 | 1     | 11             | 0                       | 11            | 1650     | 165                 | 0               | 0                            |
| 117456         | 2017 | 1     | 1              | 1                       | 2             | 2852     | 285                 | 0               | 0                            |
| 117460         | 2017 | 1     | 11             | 4                       | 15            | 2655     | 265                 | 0               | 0                            |
| 117482         | 2017 | 1     | 0              | 0                       | 0             | 0        | 0                   | 0               | 0                            |
| 117618         | 2017 | 1     | 6              | 0                       | 6             | 1638     | 163                 | 0               | 0                            |

## Sample Input Data 2

| Loyalty Number | Country | Province        | City           | Postal Code | Gender | Education | Salary | Marital Status | Loyalty Card | CLV    | Enrollment Type | Enrollment Year | Enrollment Month | Cancellation Year | Cancellation Month |
|----------------|---------|-----------------|----------------|-------------|--------|-----------|--------|----------------|--------------|--------|-----------------|-----------------|------------------|-------------------|--------------------|
| 100018         | Canada  | Alberta         | Edmonton       | T9G 1W3     | Female | Bachelor  | 92552  | Married        | Aurora       | 7919.2 | Standard        | 2016            | 8                | 0                  | 0                   |
| 100102         | Canada  | Ontario         | Toronto        | M1R 4K3     | Male   | College   |        | Single         | Nova         | 2887.74| Standard        | 2013            | 3                | 0                  | 0                   |
| 100140         | Canada  | British Columbia| Dawson Creek   | U5I 4F1     | Female | College   |        | Divorced       | Nova         | 2838.07| Standard        | 2016            | 7                | 0                  | 0                   |
| 100214         | Canada  | British Columbia| Vancouver      | V5R 1W3     | Male   | Bachelor  | 63253  | Married        | Star         | 4170.57| Standard        | 2015            | 8                | 0                  | 0                   |
| 100272         | Canada  | Ontario         | Toronto        | P1L 8X8     | Female | Bachelor  | 91163  | Divorced       | Star         | 6622.05| Standard        | 2014            | 1                | 0                  | 0                   |


## Sample Output Data

| Loyalty Number | Predicted Cluster | Cluster Label |
|----------------|--------------------|---------------|
| 117408         | 1                  | Grade 3       |
| 117456         | 1                  | Grade 3       |
| 117460         | 3                  | Grade 1       |
| 117482         | 0                  | Grade 4       |
| 117618         | 1                  | Grade 3       |
