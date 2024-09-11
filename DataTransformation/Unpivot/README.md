# UNPIVOT

# OVERVIEW
This script performs unpivoting, converting columns into rows.

1. Set the `table_name` variable to the name of the table that contains data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the final_table_name variable to the name of the table where the UnPivoted data will be uploaded
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")
5. Replace the columns in value_vars in the df.melt() method with your specific data columns to convert columns into rows.

