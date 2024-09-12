# FILTERING AND SUBSET

# OVERVIEW
This script filters the record based on the Given Condition

1. Set the `table_name` variable to the name of the table that contains data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the final_table_name variable to the name of the table where the filtered records will be uploaded
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")

INPUT DATA:

| Date       | Region | Product Category | Product         | Customer Name    | Sales | Cost |
|------------|--------|------------------|-----------------|------------------|-------|------|
| 05Sep2022  | East   | Stationery       | Art Supplies    | Wu Chang         | 4525  | 123  |
| 01Mar2023  | West   | Stationery       | Pins and Tacks  | Helen Magadalene | 525   | 143  |
| 02Apr2024  | Central| Grocery          | Art Supplies    | Xi Aun           | 1221  | 144  |


OUTPUT DATA(`WestRegionSales`):

| Date       | Region | Product Category | Product         | Customer Name    | Sales | Cost |
|------------|--------|------------------|-----------------|------------------|-------|------|
| 01Mar2023  | West   | Stationery       | Pins and Tacks  | Helen Magadalene | 525   | 143  |


OUTPUT DATA(`StationerySales`):

| Date       | Region | Product Category | Product         | Customer Name    | Sales | Cost |
|------------|--------|------------------|-----------------|------------------|-------|------|
| 05Sep2022  | East   | Stationery       | Art Supplies    | Wu Chang         | 4525  | 123  |
| 01Mar2023  | West   | Stationery       | Pins and Tacks  | Helen Magadalene | 525   | 143  |



OUTPUT DATA(`HighSales`):

| Date       | Region  | Product Category | Product         | Customer Name | Sales | Cost |
|------------|---------|------------------|-----------------|---------------|-------|------|
| 05Sep2022  | East    | Stationery       | Art Supplies    | Wu Chang      | 4525  | 123  |
| 02Apr2024  | Central | Grocery          | Art Supplies    | Xi Aun        | 1221  | 144  |






