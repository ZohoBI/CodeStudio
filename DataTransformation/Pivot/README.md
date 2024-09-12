# PIVOT

# OVERVIEW
This script performs pivoting and handles the addition of columns dynamically.

1. Set the `table_name` variable to the name of the table that contains data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the final_table_name variable to the name of the table where the Pivoted data will be uploaded
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")
5. Replace the Product Category column in the df.pivot_table() method with your column name to convert rows into columns.




INPUT DATA:

| Date       | Region  | Product Category | Product      | Customer Name | Sales  | Cost  |
|------------|---------|------------------|--------------|---------------|--------|-------|
| 17Aug2020  | East    | Furniture        | Clocks       | John Britto   | 272.34 | 14.58 |
| 06Aug2020  | Central | Stationery       | ArtSupplies  | Susan Juliet  | 45.31  | 12.93 |
| 13Aug2020  | West    | Stationery       | CopyPaper    | Venus Powell  | 409.51 | 40.92 |
| 03Sep2020  | West    | Grocery          | Fruits       | Rick Reed     | 1697.96| 503.41|


OUTPUT DATA:

| Region | Furniture | Grocery    | Stationery | TotalSales |
|--------|-----------|------------|------------|------------|
| Central| 17443.52  | 232572.50  | 58962.02   | 308978.04  |
| East   | 68200.55  | 414193.83  | 116498.94  | 598893.32  |
| West   | 45654.75  | 266214.82  | 80206.13   | 392075.70  |
