from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', SCOPES)
creds = flow.run_local_server(port=8080)

# Save the credentials for the next run
with open('token.json', 'w') as token:
    token.write(creds.to_json())

print("Google Calendar authentication complete. token.json created.") 