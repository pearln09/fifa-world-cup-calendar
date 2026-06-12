import json
import pickle

from googleapiclient.discovery import build

CALENDAR_ID = (
    "0dd434b0cd7ffc7983131822b42b1b932d67745f72220f63b4de775e0963611c"
    "@group.calendar.google.com"
)

# Load credentials
with open("token.pickle", "rb") as token:
    creds = pickle.load(token)

service = build(
    "calendar",
    "v3",
    credentials=creds
)

# Load fixtures
with open(
    "fixtures.json",
    "r",
    encoding="utf-8"
) as f:
    fixtures = json.load(f)

added = 0
updated = 0
skipped = 0

for match in fixtures:

    match_id = match["match_id"]

    home = match["home"]
    away = match["away"]

    home_score = match.get(
        "home_score"
    )

    away_score = match.get(
        "away_score"
    )

    stage = match.get(
        "stage",
        ""
    )

    group = match.get(
        "group",
        ""
    )

    stadium = match.get(
        "stadium",
        ""
    )

    match_time = match.get(
        "match_time",
        ""
    )

    # Title

    if (
        home_score is not None
        and away_score is not None
    ):

        title = (
            f"🏆 {home} "
            f"{home_score}-{away_score} "
            f"{away}"
        )

    else:

        title = (
            f"⚽ {home} vs {away}"
        )

    # Description

    description = (
        f"🏆 FIFA World Cup 2026\n\n"
        f"Match: {home} vs {away}\n"
        f"Stage: {stage}\n"
        f"Group: {group}\n"
        f"Venue: {stadium}\n"
        f"Match Time: {match_time}\n\n"
        f"FIFA Match ID: {match_id}"
    )

    start_time = match["start"]
    end_time = match["end"]

    existing_events = (
        service.events()
        .list(
            calendarId=CALENDAR_ID,
            privateExtendedProperty=[
                f"fifaMatchId={match_id}"
            ]
        )
        .execute()
    )

    if existing_events["items"]:

        event = existing_events["items"][0]

        changed = False

        if (
            event.get("summary")
            != title
        ):
            event["summary"] = title
            changed = True

        if (
            event.get("description")
            != description
        ):
            event["description"] = description
            changed = True

        if (
            event["start"]["dateTime"]
            != start_time
        ):
            event["start"]["dateTime"] = start_time
            changed = True

        if (
            event["end"]["dateTime"]
            != end_time
        ):
            event["end"]["dateTime"] = end_time
            changed = True

        if changed:

            service.events().update(
                calendarId=CALENDAR_ID,
                eventId=event["id"],
                body=event
            ).execute()

            updated += 1

        else:

            skipped += 1

    else:

        event = {
            "summary": title,

            "description": description,

            "start": {
                "dateTime": start_time
            },

            "end": {
                "dateTime": end_time
            },

            "extendedProperties": {
                "private": {
                    "fifaMatchId": match_id
                }
            },

            "reminders": {
                "useDefault": False,
                "overrides": [
                    {
                        "method": "popup",
                        "minutes": 1440
                    },
                    {
                        "method": "popup",
                        "minutes": 60
                    }
                ]
            }
        }

        service.events().insert(
            calendarId=CALENDAR_ID,
            body=event
        ).execute()

        added += 1

print()
print("==========")
print(f"Added: {added}")
print(f"Updated: {updated}")
print(f"Skipped: {skipped}")
print("==========")