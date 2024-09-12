# Project Management Budget Overrun Prediction
## Overview

This script predicts whether a project will exceed estimated budget based on other details of the project.

1. Set the `table_name` variable to the name of the table that contains data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the `final_table_name` variable to the name of the table where the output data will be uploaded
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")

INPUT DATA:

| Budget   | NumAgents | ProjectType           | Location       | ClientType | PlannedHours | PlannedDays | ActualHours | ActualDays | NumIssues | ProjectDifficulty | Urgency | ScopeChanges | TeamExperienceLevel | VendorReliabilityCategory | MarketFluctuation | BudgetOverrun |
|----------|-----------|-----------------------|----------------|------------|--------------|-------------|-------------|------------|-----------|-------------------|---------|--------------|---------------------|--------------------------|-------------------|---------------|
| 43708.61 | 44        | Software Development  | Seattle        | Government  | 1710.75      | 213.84      | 2354.29     | 294.29     | 16        | 2                 | 9       | 0            | Low                 | Medium                   | 0.960             | 1             |
| 95564.29 | 11        | Research Project      | Seattle        | Private     | 1341.34      | 167.67      | 1393.52     | 174.19     | 16        | 9                 | 8       | 2            | High                | High                     | 0.982             | 1             |
| 75879.45 | 36        | Construction          | Seattle        | Non-Profit  | 1904.29      | 238.04      | 2542.68     | 317.83     | 5         | 9                 | 6       | 6            | Medium              | Medium                   | 0.974             | 1             |
| 63879.26 | 23        | Research Project      | Austin         | Private     | 1715.50      | 214.44      | 2138.15     | 267.27     | 13        | 5                 | 8       | 9            | Low                 | Medium                   | 1.026             | 1             |
| 24041.68 | 10        | Software Development  | San Francisco  | Private     | 734.36       | 91.80       | 1079.91     | 134.99     | 13        | 6                 | 6       | 8            | Medium              | Low                      | 1.000             | 1             |


OUTPUT DATA:

| Budget   | NumAgents | PlannedHours | PlannedDays | ActualHours | ActualDays | NumIssues | ProjectDifficulty | Urgency | ScopeChanges | TeamExperienceLevel | VendorReliabilityCategory | MarketFluctuation | BudgetOverrun | Predicted_Budget_Overrun |
|----------|-----------|--------------|-------------|-------------|------------|-----------|-------------------|---------|--------------|---------------------|--------------------------|-------------------|---------------|-------------------------|
| 24796.50 | 17        | 586.92       | 73.36       | 836.13      | 104.52     | 0         | 5                 | 5       | 5            | Medium              | Medium                   | 0.955             | No            | No                      |
| 42232.57 | 28        | 1216.39      | 152.05      | 1783.28     | 222.91     | 11        | 3                 | 6       | 5            | Low                 | Medium                   | 0.964             | Yes           | Yes                     |
| 49061.74 | 37        | 1257.11      | 157.14      | 1123.55     | 140.44     | 12        | 4                 | 5       | 2            | High                | Medium                   | 1.021             | No            | No                      |
| 65427.69 | 43        | 1275.31      | 159.41      | 1247.43     | 155.93     | 13        | 4                 | 5       | 2            | Low                 | Medium                   | 0.967             | No            | No                      |

