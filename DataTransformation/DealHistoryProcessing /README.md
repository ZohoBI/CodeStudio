# Deal History Processing Sample

## Overview

This script adds previous stage and next stage for CRM Deal History.

Usage

1. Set the `table_names` variable to the list of table names containing sales data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from each table.
3. Set the `final_table_name` variable to the name of the table where the combined data will be uploaded
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")
