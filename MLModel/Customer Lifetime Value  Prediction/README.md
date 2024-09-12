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

## Sample Input Data

| Customer | State      | Customer Lifetime Value | Response | Coverage | Education | Effective To Date | EmploymentStatus | Gender | Income | Location Code | Marital Status | Monthly Premium Auto | Months Since Last Claim | Months Since Policy Inception | Number of Open Complaints | Number of Policies | Policy Type   | Policy      | Renew Offer Type | Sales Channel | Total Claim Amount | Vehicle Class | Vehicle Size |
|----------|------------|-------------------------|----------|----------|-----------|-------------------|------------------|--------|--------|---------------|----------------|-----------------------|--------------------------|------------------------------|---------------------------|--------------------|---------------|-------------|------------------|---------------|---------------------|---------------|--------------|
| BU79786  | Washington | 2763.519279             | No       | Basic    | Bachelor  | 02/24/11          | Employed          | F      | 56274  | Suburban      | Married        | 69                    | 32                       | 5                            | 0                         | 1                  | Corporate Auto | Corporate L3 | Offer1           | Agent         | 384.811147          | Two-Door Car  | Medsize      |
| QZ44356  | Arizona    | 6979.535903             | No       | Extended | Bachelor  | 01/31/11          | Unemployed        | F      | 0      | Suburban      | Single         | 94                    | 13                       | 42                           | 0                         | 8                  | Personal Auto | Personal L3 | Offer3           | Agent         | 1131.464935         | Four-Door Car | Medsize      |
| AI49188  | Nevada     | 12887.43165             | No       | Premium  | Bachelor  | 02/19/11          | Employed          | F      | 48767  | Suburban      | Married        | 108                   | 18                       | 38                           | 0                         | 2                  | Personal Auto | Personal L3 | Offer1           | Agent         | 566.472247          | Two-Door Car  | Medsize      |
| WW63253  | California | 7645.861827             | No       | Basic    | Bachelor  | 01/20/11          | Unemployed        | M      | 0      | Suburban      | Married        | 106                   | 18                       | 65                           | 0                         | 7                  | Corporate Auto | Corporate L2 | Offer1           | Call Center   | 529.881344          | SUV           | Medsize      |
| HB64268  | Washington | 2813.692575             | No       | Basic    | Bachelor  | 02/03/2011         | Employed          | M      | 43836  | Rural         | Single         | 73                    | 12                       | 44                           | 0                         | 1                  | Personal Auto | Personal L1 | Offer1           | Agent         | 138.130879          | Four-Door Car | Medsize      |

## Sample Output Data

| Customer | Predicted Data |
|----------|----------------|
| AM30008  | 13,354.79      |
| AP52565  | 6,668.92       |
| BC43958  | 7,302.42       |
| BC66536  | 6,771.26       |
| BL93527  | 2,981.68       |