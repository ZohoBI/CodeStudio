# LABELENCODING

# OVERVIEW
This script converts the categorical data into numerical data using `LabelEncoding` and uploads the updated data back into the Zoho Analytics workspace.

1. Set the `table_name` variable to the name of the table that contains the categorical data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the `final_table_name` variable to the name of the table where the converted numerical data will be uploaded.
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")
5. Replace the `Fruit` column with the name of your categorical column in the fruit_encoder.fit_transform(df['Fruit']) .

