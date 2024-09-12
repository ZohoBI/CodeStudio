# INTEREST_CALCULATOR

# OVERVIEW
This script calculates the interest amount earned for each year based on the provided principal amount, interest rate.

1. Set the `table_name` variable to the name of the table that contains Interest data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the final_table_name variable to the name of the table where the data including the interest amount , total amount be uploaded.
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")

INPUT DATA:

| Entity       | Amount | Year | Interest |
|--------------|--------|------|----------|
| mutualFunds  | 20000  | 2020 | 10       |
| Stocks       | 10000  | 2020 | 15       |
| Stocks       | 10000  | 2021 | -5       |
| mutualFunds  | 20000  | 2021 | 10       |
| Stocks       | 10000  | 2022 | 10       |
| mutualFunds  | 20000  | 2022 | -10      |


OUTPUT DATA:

| Entity       | Amount | Year | Interest | Initial_Amount | Final_Amount | Difference_In_Amount |
|--------------|--------|------|----------|----------------|--------------|----------------------|
| Stocks       | 10000  | 2020 | 15       | 10000          | 11500        | 1500                 |
| Stocks       | 10000  | 2021 | -5       | 21500          | 20425        | -1075                |
| Stocks       | 10000  | 2022 | 10       | 30425          | 33467.5      | 3042.5               |
| mutualFunds  | 20000  | 2020 | 10       | 20000          | 22000        | 2000                 |
| mutualFunds  | 20000  | 2021 | 10       | 42000          | 46200        | 4200                 |
| mutualFunds  | 20000  | 2022 | -10      | 66200          | 59580        | -6620                |

