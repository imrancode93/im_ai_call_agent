import os
from dotenv import load_dotenv
from langchain.tools import Tool
from serpapi import GoogleSearch
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import dateparser

load_dotenv()

# --- Web Search Tool (SerpAPI) ---
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def serpapi_search(query: str) -> str:
    params = {
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "engine": "google",
        "num": 3
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    if "organic_results" in results:
        return "\n".join([f"{r['title']}: {r['link']}" for r in results["organic_results"][:3]])
    return "No results found."

# --- Calendar Tool (Google Calendar API) ---
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def schedule_event(summary: str, start_time: str = None, duration_minutes: int = 30) -> str:
    """
    Schedule an event in Google Calendar.
    If start_time is not provided, attempts to parse it from the summary.
    Handles both ISO 8601 and natural language date/time strings.
    """
    # Try to extract start_time if not provided
    if not start_time:
        # Try to extract a date/time from the summary using dateparser
        dt = dateparser.parse(summary)
        if not dt:
            return "Could not determine event time from the provided information. Please specify a date and time."
    else:
        # Try ISO 8601 first
        try:
            dt = datetime.fromisoformat(start_time)
        except ValueError:
            # Fallback to dateparser
            dt = dateparser.parse(start_time)
        if not dt:
            return "Could not determine event time from the provided information. Please specify a date and time."

    end_time = dt + timedelta(minutes=duration_minutes)
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    event = {
        'summary': summary,
        'start': {
            'dateTime': dt.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'UTC',
        },
    }
    try:
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created: {event_result.get('htmlLink')}"
    except Exception as e:
        return f"Failed to create event: {e}"

calendar_tool = Tool(
    name="Calendar",
    func=schedule_event,
    description="Schedules a meeting or demo in Google Calendar. Input should include the meeting summary and date/time (ISO 8601 or natural language)."
)

tools = [
    Tool(
        name="Web Search",
        func=serpapi_search,
        description="Searches the web for real-time information about competitors, products, or market trends. Input should be a search query."
    ),
    calendar_tool
] 