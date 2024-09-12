# DUPLCIATE_HANDLING_ROW_WISE

# OVERVIEW
This Script removes the duplicate records based on the choosen coulmns

1. Set the `table_name` variable to the name of the table that contains the duplicate data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the final_table_name variable to the name of the table where the data with duplicate records removed will be uploaded
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")


INPUT DATA:

| OrderId | ProductId | Quantity | Price | Date        |
|---------|-----------|----------|-------|-------------|
| 5       | 1698      | 1        | 54.62 | 05 Jan 2023 |
| 4       | 1548      | 34       | 2132  | 05 Aug 2023 |
| 5       | 1698      | 1        | 54.62 | 05 Jan 2023 |


OUTPUT DATA:

| OrderId | ProductId | Quantity | Price | Date        |
|---------|-----------|----------|-------|-------------|
| 5       | 1698      | 1        | 54.62 | 05 Jan 2023 |
| 4       | 1548      | 34       | 2132  | 05 Aug 2023 |


