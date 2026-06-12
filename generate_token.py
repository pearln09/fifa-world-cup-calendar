from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]

flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json",
    SCOPES
)

creds = flow.run_local_server(port=8080)

with open("token.pickle", "wb") as token:
    pickle.dump(creds, token)

print("Token saved!")