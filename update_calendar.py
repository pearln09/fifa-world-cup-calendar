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

    title = (
        f"{match['home']} vs {match['away']}"
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

        if event["summary"] != title:
            event["summary"] = title
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