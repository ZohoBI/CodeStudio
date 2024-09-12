# Multi-Variate Forecasting
## Overview

This script forecasts the revenue for the specified time period,
based on other details regarding the business

1. Set the `table_name` variable to the name of the table that contains data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the `final_table_name` variable to the name of the table where the output data will be uploaded
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")


INPUT DATA:

| Date       | Amount | CROSS SELL | NEW | REACTIVATE | RECURRING | REFUND | UPGRADE | OFFLINE | ONLINE | Direct | Reseller | ANZ | APAC | Antarctica | Brazil | Canada | China | ConEurope | India | India Central | India East | India North | India South | India West | Japan | LATAM | MEA | Others | UK | US | US Central | US East | US MST | US West |
|------------|--------|------------|-----|------------|-----------|--------|---------|---------|--------|--------|----------|-----|------|------------|--------|--------|-------|-----------|-------|---------------|------------|-------------|-------------|------------|-------|-------|-----|--------|----|----|------------|---------|--------|---------|
| 2007-01-28 | 4      | 0          | 1   | 1          | 1         | 0      | 1       | 1       | 3      | 4      | 0        | 0   | 0    | 0          | 0      | 0      | 0     | 0         | 1     | 0             | 0          | 0           | 0           | 0          | 0     | 1     | 0   | 0      | 0  | 2  | 0          | 0       | 0      | 0       |
| 2006-11-26 | 12     | 0          | 0   | 0          | 1         | 0      | 0       | 0       | 1      | 1      | 0        | 0   | 0    | 0          | 0      | 0      | 0     | 0         | 1     | 0             | 0          | 0           | 0           | 0          | 0     | 0     | 0   | 0      | 0  | 0  | 0          | 0       | 0      | 0       |
| 2007-02-11 | 85     | 0          | 1   | 0          | 1         | 0      | 0       | 0       | 2      | 2      | 0        | 0   | 0    | 0          | 0      | 0      | 0     | 0         | 1     | 0             | 0          | 0           | 0           | 0          | 0     | 0     | 0   | 0      | 0  | 1  | 0          | 0       | 0      | 0       |
| 2007-03-18 | 110    | 0          | 2   | 0          | 4         | 0      | 0       | 0       | 6      | 6      | 0        | 1   | 0    | 0          | 0      | 0      | 0     | 1         | 0     | 4             | 0          | 0           | 0           | 0          | 0     | 0     | 0   | 0      | 0  | 0  | 0          | 0       | 0      | 0       |
| 2007-04-15 | 111    | 0          | 5   | 0          | 2         | 0      | 0       | 0       | 7      | 7      | 0        | 1   | 1    | 0          | 0      | 0      | 0     | 0         | 4     | 0             | 0          | 0           | 0           | 0          | 0     | 0     | 0   | 0      | 0  | 0  | 0          | 0       | 0      | 0       |
| 2007-03-11 | 145    | 0          | 3   | 0          | 3         | 0      | 0       | 0       | 6      | 5      | 1        | 0   | 0    | 0          | 1      | 0      | 0     | 0         | 3     | 0             | 0          | 0           | 0           | 0          | 0     | 0     | 0   | 0      | 0  | 1  | 0          | 0       | 0      | 0       |


OUTPUT DATA:

| Date                | Amount        | CROSS SELL | NEW    | REACTIVATE | RECURRING | REFUND | UPGRADE | OFFLINE | ONLINE | Direct  | Reseller | ANZ     | APAC    | Antarctica | Brazil  | Canada | China  | ConEurope | India  | India Central | India East | India North | India South | India West | Japan   | LATAM   | MEA    | Others | UK    | US    | US Central | US East | US MST | US West |
|---------------------|---------------|------------|--------|------------|-----------|--------|---------|---------|--------|---------|----------|---------|---------|------------|---------|--------|--------|-----------|--------|---------------|------------|-------------|-------------|------------|---------|---------|--------|--------|-------|-------|------------|---------|--------|---------|
| 2023-08-20 00:00:00 | 129364169.082 | 6529.547   | 6429.549 | 7399.898  | 18382.338 | 2845.752 | 7245.074 | 5616.199 | 43240.534 | 36289.037 | 12569.088 | 2170.053 | 3786.951 | 0.494      | 580.559  | 1001.019 | 514.94   | 13865.321 | 1395.485  | 529.993      | 345.719    | 1410.195    | 610.925     | 1022.632   | 300.586  | 6559.289 | 7819.069 | 36.907 | 1320.552 | 541.631  | 1472.553 | 1275.984 | 1069.648 |
| 2023-09-17 00:00:00 | 136247035.37  | 3257.673   | 3839.491 | 2141.211  | 10719.961 | 593.566 | 6494.137 | 5142.483 | 21914.439 | 18870.035 | 8166.829  | 1041.71  | 3282.796 | 0.711      | 160.49   | 297.611  | 120.018  | 6357.075  | 947.152   | 252.907      | 374.954    | 570.943     | 646.272     | 898.207    | 283.349  | 3201.868 | 6643.305 | 79.307 | 643.088  | 522.276  | 148.519  | 1015.058 | 566.005  |
| 2023-08-27 00:00:00 | 59856429.755  | 845.139    | 3136.281 | 711.824   | 5371.878  | 197.713 | 699.88   | 1009.046 | 9961.166  | 6531.238  | 4465.334  | 101.98   | 939.994  | 1.911      | 343.199  | 259.872  | 16.592   | 5373.892  | 182.411   | 37.394       | 260.517    | 192.687     | 89.898      | 140.327    | 220.487  | 3309.678 | 1466.26  | 153.338 | 204.653  | 348.928  | 738.178  | 309.697  | 79.657   |
| 2023-09-24 00:00:00 | 44071241.223  | 3723.585   | 837.204  | 2515.634  | 2993.872  | 617.461 | 2093.125 | 1713.602 | 11093.289 | 8189.89   | 4608.093  | 395.79   | 2956.584 | 0.829      | 33.115   | 40.261   | 125.126  | 4674.357  | 479.972   | 90.798       | 274.703    | 243.986     | 51.086      | 311.611    | 130.15   | 1166.727 | 4501.596 | 138.402 | 223.541  | 228.456  | 390.613  | 6.948    | 352.888  |
| 2023-08-13 00:00:00 | 238128431.794 | 2461.112   | 2560.699 | 3855.954  | 22873.092 | 553.871 | 6913.023 | 3263.094 | 35975.502 | 27520.841 | 11690.997 | 1573.975 | 3707.838 | 4.26       | 920.029  | 1760.003 | 412.816  | 7742.436  | 676.92    | 247.107      | 483.823    | 189.308     | 1633.337    | 1485.387   | 340.932  | 6400.797 | 4953.098 | 259.481 | 1284.036 | 202.502  | 2053.984 | 2728.652 | 851.797  |