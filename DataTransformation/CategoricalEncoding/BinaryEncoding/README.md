# BINARYENCODING

# OVERVIEW 
This script converts the categorical data into numerical data using `BINARYENCODING` and uploads the updated data back into the Zoho Analytics workspace.

1. Set the `table_name` variable to the name of the table that contains the categorical data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the `final_table_name` variable to the name of the table where the converted numerical data will be uploaded.
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")


INPUT DATA:

| ID | Feedback Sentiment |
|----|--------------------|
| 2  | Mixed              |
| 6  | Very Positive      |
| 10 | Negative           |
| 14 | Very Negative      |
| 18 | Neutral            |
| 22 | Positive           |



OUTPUT DATA:

| ID | Feedback Sentiment | Bit1 | Bit2 | Bit3 |
|----|--------------------|------|------|------|
| 2  | Mixed              | 1    | 0    | 1    |
| 6  | Very Positive      | 0    | 1    | 1    |
| 10 | Negative           | 0    | 1    | 0    |
| 14 | Very Negative      | 1    | 0    | 0    |
| 18 | Neutral            | 0    | 0    | 1    |
| 22 | Positive           | 0    | 0    | 0    |




