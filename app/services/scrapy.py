import requests
from bs4 import BeautifulSoup



def test_scrap_web():
    return 'Scraping SBM Test Env'


def test_download_rate_sheet():
    return "MCB Rate sheet"


def scrape_web():

    results = []
    # URL of the exchange rates page
    url = "https://banking.sbmgroup.mu/individual/exchange-rate"

    # Fetch the page content
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        # Locate the exchange rates table (adjust the selector as needed)
        table = soup.find("table")  # Assuming it's the first table on the page

        # Check if the table was found
        if table:
            rows = table.find_all("tr")  # Find all rows in the table
        else:
            print("No table found on the page")
            rows = []
        # Parse the table rows
        exchange_rates = []
        for row in rows:
            cells = row.find_all("td")  # Assuming data is within <td> tags
            if cells:  # Skip headers or empty rows
                currency = cells[2].get_text(strip=True)
                buying_rate = cells[3].get_text(strip=True)
                selling_rate = cells[6].get_text(strip=True)
                country = cells[1].get_text(strip=True)
                date_forex = cells[0].get_text(strip=True)
                exchange_rates.append(
                    {
                        "Currency": currency,
                        "Buying Rate": buying_rate,
                        "Selling Rate": selling_rate,
                        "Country": country,
                        "Date": date_forex
                    }
                )

        # Print the results
        for rate in exchange_rates:
            print(rate)
            results.append(rate)
    else:
            results = ["Failed to fetch the page. Status code: {response.status_code}"]
    return results
