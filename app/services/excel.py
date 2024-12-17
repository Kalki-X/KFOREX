
import requests



def get_ratesheets():

    # The URL endpoint for downloading the file (update after inspecting the network request)
    url = "https://mcb.mu/webapi/mcb/ForexDataExcel"

    # Data to be sent in the request (update based on the inspected request parameters)
    payload = {
        "BaseCurrency": "MUR",  # Example currency
        "CurrencyCode": "ALL",
        "EndDate": "2024-12-17",
        "StartDate": "2024-12-17"
    }

    # Headers (optional, depending on what the server expects)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",  # Adjust based on the request
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    # Path to save the downloaded file
    save_path = "exchange_rates.xlsx"

    try:
        # Send the request
        response = requests.post(url, data=payload, headers=headers)

        # Check if the request was successful
        if response.status_code == 200 and "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in response.headers.get("Content-Type", ""):
            print(response.content)
            # Save the file
            with open(save_path, "wb") as file:
                file.write(response.content)
            print(f"File downloaded successfully and saved as '{save_path}'.")
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
