# HANDLING MISSING DATA

# OVERVIEW
This script handles the missing data based on mean,median,mode

1. Set the `table_name` variable to the name of the table that contains missing value data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the final_table_name variable to the name of the table where the data, with missing values replaced, will be uploaded.
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")
5. Replace the age column with the column from your data that contains missing values.