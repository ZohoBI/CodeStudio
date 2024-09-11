# PIVOT

# OVERVIEW
This script performs pivoting and handles the addition of columns dynamically.

1. Set the `table_name` variable to the name of the table that contains data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the final_table_name variable to the name of the table where the Pivoted data will be uploaded
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")
5. Replace the Product Category column in the df.pivot_table() method with your column name to convert rows into columns.