import os
from datetime import datetime, timedelta
import requests
from cryptography.fernet import Fernet
import pandas as pd
import json
import threading


# Define the path to the JSON file
json_file_path = 'app/models/mcdb.json'

def exclude_weekend():
    current_date = datetime.now()
    if current_date.weekday() == 5:
        current_date = current_date - timedelta(days=1)
    elif current_date.weekday() == 6:
        current_date = current_date - timedelta(days=2)
    else:
        current_date = current_date
    return current_date.strftime("%Y-%m-%d")

def get_ratesheets():

    results = []

    # Retrieve the key from environment variables
    key_hash_id = os.getenv('KEY_HASH_ID')
    key_hash_uri = os.getenv('KEY_HASH_URI')

    if key_hash_id and key_hash_uri:

        fernet = Fernet(key_hash_id.encode())

        try:
            decrypt_url = fernet.decrypt(key_hash_uri.encode()).decode()
        except Exception as e:
            results.append(f"An error occurred during decryption: {e}")
            return results

        # The URL endpoint for downloading the file (update after inspecting the network request)
        url = str(decrypt_url)

        # Data to be sent in the request (update based on the inspected request parameters)
        payload = {
            "BaseCurrency": "MUR",  # Example currency
            "CurrencyCode": "ALL",
            "EndDate": exclude_weekend(),
            "StartDate": exclude_weekend()
        }

        # Headers (optional, depending on what the server expects)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",  # Adjust based on the request
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }

        # Path to save the downloaded file
        save_path = "./docs/exchange_rates.xlsx"

        try:
            # Send the request
            response = requests.post(url, data=payload, headers=headers)

            # Check if the request was successful
            if response.status_code == 200 and "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in response.headers.get("Content-Type", ""):
                # Save the file
                with open(save_path, "wb") as file:
                    file.write(response.content)
                    print(f"File downloaded successfully and saved as '{save_path}'.")
                excel_line()
            else:
                results.append(f"Failed to download the file. Status code: {response.status_code}")
        except Exception as e:
            results.append(f"An error occurred: {e}")
    else:
        results.append("KFX: Fatal Err in hashing val.")

    return results

def excel_line():

    # Load the Excel file
    file_path = './docs/exchange_rates.xlsx'  # Make sure the file is in the same directory as this script
    df = pd.read_excel(file_path, sheet_name='Indicative Rates', skiprows=6)

    # Rename the columns for clarity
    df.columns = [
        'Country', 'Currency', 'Code', 'Units', 'Buying_TT', 'Buying_TC_DD',
        'Buying_Notes', 'Selling_TT', 'Selling_TC_DD', 'Selling_Notes', 'Rate_Date'
    ]

    # Filter out rows without country or code information
    df_rates = df[df['Country'].notna() & df['Code'].notna()]

    # Select relevant columns
    df_output = df_rates[['Country', 'Code', 'Buying_TT', 'Buying_TC_DD', 'Selling_TT', 'Selling_TC_DD', 'Rate_Date']]

    # Create an empty list to store the results
    result_list = []

    # Iterate over each row and match corresponding values
    for index, row in df_output.iterrows():
        result = {
            'Index': int(index),  # Ensure the index is an integer
            'Country': str(row['Country']),  # Convert to string to avoid type issues
            'Code': str(row['Code']),
            'Buying TT': row['Buying_TT'] if pd.notnull(row['Buying_TT']) else 'N/A',
            'Buying TC/DD': row['Buying_TC_DD'] if pd.notnull(row['Buying_TC_DD']) else 'N/A',
            'Selling TT': row['Selling_TT'] if pd.notnull(row['Selling_TT']) else 'N/A',
            'Selling TC/DD': row['Selling_TC_DD'] if pd.notnull(row['Selling_TC_DD']) else 'N/A',
            'Rate_Date': row['Rate_Date'] if pd.notnull(row['Rate_Date']) else 'N/A'

        }
        result_list.append(result)

    print(os.path.getsize(json_file_path))

    # Convert the list of dictionaries to a JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(result_list, json_file, indent=4)

    return (f"Data has been successfully stored in {json_file_path}")

def get_jsonrates():
    with open(json_file_path, 'r') as json_file:
        try:
            data = json.load(json_file)
            return data
        except json.JSONDecodeError:
            print("The JSON file is not valid.")
            return None


def main_mrates():
    # Check if the file exists and is not empty
    if os.path.exists(json_file_path) and os.path.getsize(json_file_path) > 0:
        print("Rates from JSON")
        return get_jsonrates()
    else:
      return get_ratesheets()
      print("Rates from API REQUEST")
