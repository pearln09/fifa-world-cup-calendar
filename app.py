import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]

st.title("⚽ FIFA World Cup 2026 Calendar Sync")

if st.button("Sync World Cup Matches"):

    # Google Authentication
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json",
        SCOPES
    )

    creds = flow.run_local_server(port=8080)

    st.success("Successfully authenticated!")

    # Connect to Google Calendar
    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    # Look for existing FIFA calendar
    calendar_id = None

    calendars = service.calendarList().list().execute()

    for cal in calendars["items"]:
        if cal["summary"] == "⚽ FIFA World Cup 2026":
            calendar_id = cal["id"]
            break

    # Create calendar if it doesn't exist
    if calendar_id is None:

        calendar = {
            "summary": "⚽ FIFA World Cup 2026",
            "timeZone": "Asia/Kolkata"
        }

        created_calendar = (
            service.calendars()
            .insert(body=calendar)
            .execute()
        )

        calendar_id = created_calendar["id"]

        st.success("Created FIFA calendar!")

    else:
        st.success("Using existing FIFA calendar!")

    # Sample matches
    matches = [
        {
            "home": "Argentina",
            "away": "Brazil",
            "start": "2026-06-15T20:00:00+05:30",
            "end": "2026-06-15T22:00:00+05:30"
        },
        {
            "home": "France",
            "away": "Germany",
            "start": "2026-06-16T20:00:00+05:30",
            "end": "2026-06-16T22:00:00+05:30"
        },
        {
            "home": "Spain",
            "away": "England",
            "start": "2026-06-17T20:00:00+05:30",
            "end": "2026-06-17T22:00:00+05:30"
        }
    ]

    # Add matches
    for match in matches:

        event_title = (
            f"{match['home']} vs {match['away']}"
        )

        existing_events = (
            service.events()
            .list(
                calendarId=calendar_id,
                q=event_title
            )
            .execute()
        )

        if existing_events["items"]:
            st.info(
                f"Skipped: {event_title}"
            )
            continue

        event = {
            "summary": event_title,
            "start": {
                "dateTime": match["start"]
            },
            "end": {
                "dateTime": match["end"]
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {
                        "method": "popup",
                        "minutes": 60
                    }
                ]
            }
        }

        service.events().insert(
            calendarId=calendar_id,
            body=event
        ).execute()

        st.success(
            f"Added: {event_title}"
        )