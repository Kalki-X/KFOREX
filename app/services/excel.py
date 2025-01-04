import os
import datetime
import requests
from cryptography.fernet import Fernet


get_date = datetime.datetime.now()
get_current_date = get_date.strftime("%Y-%m-%d")

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
            "EndDate": get_current_date,
            "StartDate": get_current_date
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
                results.append(f"File downloaded successfully and saved as '{save_path}'.")
            else:
                results.append(f"Failed to download the file. Status code: {response.status_code}")
        except Exception as e:
            results.append(f"An error occurred: {e}")
    else:
        results.append("KFX: Fatal Err in hashing val.")

    return results
