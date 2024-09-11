# DATE_TIME_EXTRACTION

# OVERVIEW
This script extracts date and time data from the table in Zoho Analytics, converts it into numerical columns, and uploads the updated data back into the Zoho Analytics workspace.

1. Set the `table_name` variable to the name of the table that contains the datetime data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the `final_table_name` variable to the name of the table where the extracted numerical data will be uploaded
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")
5. Replace the DateTime column name with the name of the column in your table that has the datetime data.