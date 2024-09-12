# Inventory Demand Forecasting
## Overview: 
This script predicts the demand for the next required period(s)

1. Set the `table_name` variable to the name of the table that contains data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the `final_table_name` variable to the name of the table where the output data will be uploaded
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")

INPUT DATA: 

| Date       | Store | Item | Sales |
|------------|-------|------|-------|
| 2013-01-01 | 1     | 1    | 13    |
| 2013-01-02 | 1     | 1    | 11    |
| 2013-01-03 | 1     | 1    | 14    |


OUTPUT DATA:

| Forecasted Demand | date       | sales | store | item | month | day_of_month | day_of_year | day_of_week | year | is_wknd | is_month_start | is_month_end |
|-------------------|------------|-------|-------|------|-------|--------------|-------------|-------------|------|---------|----------------|--------------|
| 17.73             | 2017-01-01 | 19    | 1     | 1    | 1     | 1            | 1           | 6           | 2017 | 1       | 1              | 0            |
| 10.43             | 2017-01-02 | 15    | 1     | 1    | 1     | 2            | 2           | 0           | 2017 | 0       | 0              | 0            |
| 12.10             | 2017-01-03 | 10    | 1     | 1    | 1     | 3            | 3           | 1           | 2017 | 0       | 0              | 0            |
| 12.10             | 2017-01-04 | 16    | 1     | 1    | 1     | 4            | 4           | 2           | 2017 | 0       | 0              | 0            |
