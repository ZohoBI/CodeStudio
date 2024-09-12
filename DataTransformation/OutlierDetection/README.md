# OUTLIER DETECTION

# OVERVIEW
This script identifies outliers in the provided dataset.

1. Set the `table_name` variable to the name of the table that contains data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the final_table_name variable to the name of the table where the Outlier data will be uploaded
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")
5. Replace the `Sales` data in the `self.detect_outliers_zscore(df, 'Sales', 2)` method with the name of your specific data column.

INPUT DATA:

| ID | SALES |
|----|-------|
| 1  | 1222  |
| 2  | 1200  |
| 3  | 1201  |
| 4  | 1301  |
| 5  | 1242  |
| 6  | 1244  |
| 7  | 10000 |

OUTPUT DATA:

| ID | SALES |
|----|-------|
| 7  | 10000 |
