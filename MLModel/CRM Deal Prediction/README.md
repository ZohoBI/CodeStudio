# CRM Deal Prediction
## Overview: 
This script predicts whether a deal might be converted or not using historical CRM data.

1. Set the `table_name` variable to the name of the table that contains data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the `final_table_name` variable to the name of the table where the output data will be uploaded
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")

INPUT DATA:

| Deal ID                  | Amount | Deal Name | Closing Date | Stage      | Type             | Probability (%) | Expected Revenue | Lead Source   | Created Time        | Modified Time       | Sales Cycle Duration |
|--------------------------|--------|-----------|--------------|------------|------------------|-----------------|------------------|---------------|---------------------|---------------------|----------------------|
| zcrm_689437000004952714   | 10000  | New Deal  | 26/03/2023   | Closed Won | New Business      | 100             | 10000.0          | Advertisement | 29/11/2022 13:02    | 29/11/2022 13:02    | 117                  |
| zcrm_689437000004952734   | 234500 | Deal17    | 31/01/2023   | Closed Won | Existing Business | 100             | 234500.0         | Partner       | 29/11/2022 13:02    | 29/11/2022 13:02    | 63                   |
| zcrm_689437000004952736   | 50000  | Deal17dd  | 26/02/2023   | Closed Won | Existing Business | 100             | 50000.0          | Partner       | 29/11/2022 13:02    | 29/11/2022 13:02    | 89                   |
| zcrm_689437000004952751   | 0      | uyyvghj   | 03/05/2023   | Closed Won | New Business      | 100             | 0.0              | Partner       | 29/11/2022 13:02    | 29/11/2022 13:02    | 155                  |
| zcrm_689437000004952753   | 40000  | dfafad    | 25/03/2023   | Closed Won | New Business      | 90              | 36000.0          | Partner       | 29/11/2022 13:02    | 29/11/2022 13:02    | 116                  |


OUTPUT DATA:

| Amount | Probability (%) | Expected Revenue | Sales Cycle Duration | Type               | Lead_Source        | Stage | Deal Prediction |
|--------|-----------------|------------------|----------------------|--------------------|--------------------|-------|-----------------|
| 123456 | 80              | 98764.8          | 0                    | New Business       | Advertisement      | 1     | 1               |
| 15000  | 89              | 13350.0          | 6                    | Existing Business  | Online Store       | 0     | 1               |
| 8000   | 67              | 5360.0           | 112                  | New Business       | Partner            | 1     | 1               |
| 12000  | 0               | 0.0              | 6                    | Existing Business  | Employee Referral  | 0     | 0               |
| 14000  | 90              | 12600.0          | 6                    | Type Not Mentioned | Online Store       | 0     | 1               |
