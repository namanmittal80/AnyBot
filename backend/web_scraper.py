import requests
import json
from bs4 import BeautifulSoup
import re

# URL of the webpage you want to scrape
url = "https://www.responseinformaticsltd.com/"

# Headers to mimic a browser
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

# Step 1: Fetch the page
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Extract the raw HTML
    html_content = response.text

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract and clean the text
    cleaned_text = soup.get_text().strip()  # Add separators for readability

    # Save the cleaned HTML in JSON
    data = {"html": cleaned_text}
    
    output_file = "webpage_cleaned.json"
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    print(f"Page successfully scraped and saved to {output_file}")
else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")