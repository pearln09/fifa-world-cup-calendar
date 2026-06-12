import requests
from bs4 import BeautifulSoup

URL = "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/scores-fixtures"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)

print("Status:", response.status_code)

with open("fifa_page.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("Saved fifa_page.html")