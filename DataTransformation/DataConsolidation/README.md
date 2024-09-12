# Data Consolidation Sample

## Overview
This script combines sales data from multiple tables in Zoho Analytics and uploads the consolidated data to a single table.
Usage

1. Set the `table_names` variable to the list of table names containing sales data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from each table.
3. Set the `final_table_name` variable to the name of the table where the combined data will be uploaded
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")


INPUT DATA:

| ID | Sales    |
|----|----------|
| 1  | €6234.59 |
| 2  | €2434.59 |



| ID | Sales   |
|----|---------|
| 1  | $234.59 |
| 2  | $415.41 |


| ID | Sales   |
|----|---------|
| 1  | ₹878.32 |
| 2  | ₹718.32 |


OUTPUT DATA:

| ID | Sales    |
|----|----------|
| 1  | €6234.59 |
| 2  | €2434.59 |
| 1  | $234.59  |
| 2  | $415.41  |
| 1  | ₹878.32  |
| 2  | ₹718.32  |










