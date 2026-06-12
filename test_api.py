import requests

API_KEY = "f475e38ebdef3c433abf7ffa88b90038"

headers = {
    "x-apisports-key": API_KEY
}

response = requests.get(
    "https://v3.football.api-sports.io/fixtures",
    headers=headers,
    params={
        "live": "all"
    }
)

data = response.json()

for match in data.get("response", []):
    league = match["league"]
    print(
        f"{league['id']} - {league['name']} ({league['country']})"
    )