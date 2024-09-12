# DUPLCIATE_HANDLING_ROW_WISE

# OVERVIEW
This script removes duplicate records .

1. Set the `table_name` variable to the name of the table that contains the duplicate data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the final_table_name variable to the name of the table where the data with duplicate records removed will be uploaded
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")
5. Specify the columns in the df.drop_duplicates(subset=['brand', 'style'], keep='last') method for which duplicates will be removed based on those columns.
6. Set `keep='last'` if you want to retain the last record among duplicates, or set `keep='first'` if you want to keep the first duplicate record.


INPUT DATA:

| Brand  | Style | Rating |
|--------|-------|--------|
| Brand1 | bowl  | 2.085  |
| Brand2 | cup   | 3.430  |
| Brand1 | Bowl  | 4.434  |


OUTPUT DATA:

| Brand  | Style | Rating |
|--------|-------|--------|
| Brand2 | cup   | 3.430  |
| Brand1 | Bowl  | 4.434  |
