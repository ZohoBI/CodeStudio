# DATE_TIME_ENCODING

# OVERVIEW
This script converts the datetime data into numerical columns by `ONE HOT ENCODING` and uploads the updated data back into the Zoho Analytics workspace.

1. Set the `table_name` variable to the name of the table that contains the datetime data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the `final_table_name` variable to the name of the table where the extracted numerical data will be uploaded
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")
5. Replace the DateTime column name with the name of the column in your table that has the datetime data.


INPUT DATA:

| Event_ID | DateTime                  |
|----------|---------------------------|
| 3        | 2023-09-29 11:09:40       |
 



OUTPUT DATA:

| Event_ID | DateTime                  | MONTH1 | MONTH2 | MONTH3 | MONTH4 | MONTH5 | MONTH6 | MONTH7 | MONTH8 | MONTH9 | MONTH10 | MONTH11 | MONTH12 |
|----------|---------------------------|--------|--------|--------|--------|--------|--------|--------|--------|--------|---------|---------|---------|
| 3        | 2023-09-29 11:09:40       | 0      | 0      | 0      | 0      | 0      | 0      | 0      | 0      | 1      | 0       | 0       | 0       |

