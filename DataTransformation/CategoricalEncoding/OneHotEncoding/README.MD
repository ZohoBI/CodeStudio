# ONEHOTENCODING

# OVERVIEW
This script converts the categorical data into numerical data using `Onehotencoding` and uploads the updated data back into the Zoho Analytics workspace.

1. Set the `table_name` variable to the name of the table that contains the categorical data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the `final_table_name` variable to the name of the table where the converted numerical data will be uploaded.
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")
5. Specify the columns in the `getdummies()` method that you want to convert from categorical to numerical.


INPUT DATA:

| CustomerID | Gender | Age | ProductCategory | AmountSpent |
|------------|--------|-----|-----------------|-------------|
| 2          | Female | 49  | Books           | 182.56      |
| 6          | Female | 35  | Clothing        | 171.45      |
| 26         | Female | 50  | Electronics     | 191.18      |
| 14         | Male   | 67  | Books           | 50.91       |
| 130        | Female | 64  | Electronics     | 211.02      |


OUTPUT DATA:

| CustomerID | Age | AmountSpent | Gender_Female | Gender_Male | ProductCategory_Books | ProductCategory_Clothing | ProductCategory_Electronics |
|------------|-----|-------------|---------------|-------------|------------------------|--------------------------|-----------------------------|
| 2          | 49  | 182         | 1             | 0           | 1                      | 0                        | 0                           |
| 6          | 35  | 171         | 1             | 0           | 0                      | 1                        | 1                           |
| 26         | 50  | 191         | 1             | 0           | 0                      | 0                        | 1                           |
| 14         | 67  | 50          | 0             | 1           | 1                      | 0                        | 0                           |
| 130        | 64  | 211         | 0             | 1           | 0                      | 0                        | 1                           |




