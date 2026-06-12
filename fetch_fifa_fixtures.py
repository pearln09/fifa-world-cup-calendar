import requests
import json
from datetime import datetime, timedelta

URL = (
    "https://api.fifa.com/api/v3/calendar/matches"
    "?language=en"
    "&count=500"
    "&idSeason=285023"
)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json"
}

response = requests.get(
    URL,
    headers=headers
)

print("Status:", response.status_code)

data = response.json()

fixtures = []

for match in data["Results"]:

    try:

        if (
            match.get("Home") is None
            or match.get("Away") is None
        ):
            continue

        if (
            match["Home"].get("TeamName") is None
            or match["Away"].get("TeamName") is None
        ):
            continue

        home_team = (
            match["Home"]["TeamName"][0]["Description"]
        )

        away_team = (
            match["Away"]["TeamName"][0]["Description"]
        )

        start_time = datetime.fromisoformat(
            match["Date"].replace(
                "Z",
                "+00:00"
            )
        )

        end_time = (
            start_time +
            timedelta(hours=2)
        )

        fixtures.append(
    {
        "match_id": match["IdMatch"],

        "home": home_team,
        "away": away_team,

        "home_score": match.get(
            "HomeTeamScore"
        ),

        "away_score": match.get(
            "AwayTeamScore"
        ),

        "winner": match.get(
            "Winner"
        ),

        "match_status": match.get(
            "MatchStatus"
        ),

        "match_time": match.get(
            "MatchTime"
        ),

        "stage": (
            match["StageName"][0]["Description"]
            if match["StageName"]
            else ""
        ),

        "group": (
            match["GroupName"][0]["Description"]
            if match["GroupName"]
            else ""
        ),

        "stadium": (
            match["Stadium"]["Name"][0]["Description"]
            if match.get("Stadium")
            else ""
        ),

        "start": start_time.isoformat(),

        "end": end_time.isoformat()
    }
)

    except Exception as e:
        print("Skipped:", e)

with open(
    "fixtures.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        fixtures,
        f,
        indent=4,
        ensure_ascii=False
    )

print(
    f"Saved {len(fixtures)} fixtures."
)