# Support Ticket Escalation Prediction
## Overview

This script predicts whether a support ticket will escalate or not based on the client and few other related details that include response time, priority, ticket age, etc.
1. Set the `table_name` variable to the name of the table that contains data in Zoho Analytics.
2. Set the `column_names` variable to the list of column names to fetch from the table.
3. Set the `final_table_name` variable to the name of the table where the output data will be uploaded
4. Set the `import_type` variable to the import type for the upload (default: "truncateadd")


INPUT DATA:

| TicketID | IssueType | Priority | ResponseTime | ResolutionTime | CustomerType | TicketAge | Escalated |
|----------|-----------|----------|--------------|----------------|--------------|-----------|-----------|
| 1        | Shipping  | Low      | 0.50         | 3.27           | Business      | 5         | 0         |
| 2        | Product   | Low      | 0.70         | 6.46           | Individual    | 8         | 0         |
| 3        | Account   | High     | 1.38         | 4.16           | Enterprise    | 3         | 1         |
| 4        | Product   | Low      | 0.50         | 12.73          | Individual    | 16        | 1         |
| 5        | Product   | Medium   | 2.28         | 11.44          | Business      | 14        | 1         |


OUTPUT DATA:

| Priority | ResponseTime | ResolutionTime | TicketAge | Escalated | Predicted_Escalated | CustomerType |
|----------|--------------|----------------|-----------|-----------|---------------------|--------------|
| High     | 0.50         | 13.83          | 13        | Yes       | Yes                 | Individual   |
| High     | 1.95         | 3.49           | 5         | No        | No                  | Business     |
| Low      | 1.52         | 9.53           | 11        | No        | No                  | Business     |
| Low      | 0.50         | 4.52           | 6         | No        | No                  | Business     |
| Low      | 1.77         | 5.81           | 6         | No        | No                  | Enterprise   |
