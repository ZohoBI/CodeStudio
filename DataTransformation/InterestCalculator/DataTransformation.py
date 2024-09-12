from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
import pandas as pd

class DataTransformation:
    dt: DataTransformationUtil = None
    za: ZohoAnalytics = None

    def __init__(self, za):
        self.za = za
        self.dt = DataTransformationUtil(self.za)
        self.log = self.za.context.log

    def process_data(self):
        table_name="Investment_Data"
        column_names=["Entity", "Amount", "Year", "Interest"]
        final_table_name="Detailed Interest Calculation Summary"
        import_type="truncateadd"


        # Fetch data from Zoho Analytics table 'data'
        df: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)
        
        # Sort the DataFrame by 'Entity' and 'Year'
        df = df.sort_values(by=['Entity', 'Year']).reset_index(drop=True)

        

        # Function to calculate the initial amount, final amount, and change amount
        def calculate_amounts(df):
            # Initialize a dictionary to store the last final amount for each entity
            last_final_amount = {}

            # Lists to store the calculated initial amounts, final amounts, and change amounts
            initial_amounts = []
            final_amounts = []
            change_amounts = []

            for index, row in df.iterrows():
                entity = row['Entity']

                # If entity is not in the dictionary, set last final amount to 0
                if entity not in last_final_amount:
                    last_final_amount[entity] = 0

                # Calculate the initial amount for the current year
                initial_amount = row['Amount'] + last_final_amount[entity]

                # Calculate the final amount after applying the percentage change
                final_amount = initial_amount * (1 + row['Interest'] / 100)

                # Calculate the change amount
                change_amount = final_amount - initial_amount

                # Store the calculated amounts
                initial_amounts.append(initial_amount)
                final_amounts.append(final_amount)
                change_amounts.append(change_amount)

                # Update the last final amount for the entity
                last_final_amount[entity] = final_amount

            # Add the new columns to the DataFrame
            df['Initial_Amount'] = initial_amounts
            df['Final_Amount'] = final_amounts
            df['Differnce_In_Amount'] = change_amounts

            return df

        # Apply the calculation function
        df = calculate_amounts(df)

        df = df.sort_values(by=['Entity', 'Year']).reset_index(drop=True)


        # Upload the processed data to Zoho Analytics table 'data_processed'
        self.dt.upload_tabledata_from_DataFrame(final_table_name, df, {"importType": import_type})

        # Log the completion of the process
        self.log.INFO("Data processing completed successfully")

