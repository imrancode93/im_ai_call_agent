from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from tools import tools, schedule_event
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

class SalesCallAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent="chat-conversational-react-description",
            memory=self.memory,
            verbose=True
        )

    def process_transcription(self, transcription: str) -> dict:
        """
        Process the transcription and let the agent use tools to generate summary, action items, and take actions.
        Returns a dict with keys: summary, action_items, calendar, web_search
        """
        try:
            # Prompt the agent to analyze the call and use tools as needed
            prompt = (
                """
                You are an expert AI sales assistant. Analyze the following sales call transcription and:
                1. Provide a concise executive summary
                2. Extract a list of specific action items
                3. If a meeting/demo/follow-up is needed, schedule it using the Calendar tool (always provide the date and time in ISO 8601 format, e.g., 2025-06-26T14:00:00)
                4. If a competitor, product, or market trend is mentioned, use the Web Search tool to find relevant info

                IMPORTANT: If you use the Web Search tool, you MUST include the search results (the Observation) in the 'Web Search' section of your final answer. Format the 'Web Search' section as a list of links and short descriptions.

                Return your results in this format:
                Executive Summary: ...
                Action Items: ...
                Calendar: ...
                Web Search: ...

                Here is the transcription:
                """ + transcription
            )
            result = self.agent.run(prompt)
            # The result is a string; parse it into a dict for the UI
            output = {"summary": "", "action_items": [], "calendar": "", "web_search": ""}
            # Simple parsing based on section headers
            for section in ["Executive Summary", "Action Items", "Calendar", "Web Search"]:
                if section in result:
                    part = result.split(section + ":", 1)[1]
                    next_section = [s for s in ["Executive Summary", "Action Items", "Calendar", "Web Search"] if s != section and s+":" in part]
                    if next_section:
                        part = part.split(next_section[0] + ":", 1)[0]
                    part = part.strip()
                    if section == "Action Items":
                        output["action_items"] = [item.strip("- ") for item in part.split("\n") if item.strip()]
                    else:
                        output[section.lower().replace(" ", "_")] = part
            # --- Calendar tool integration: actually schedule the event if needed ---
            cal = output.get("calendar", "")
            # If the calendar output is not a link and looks like a scheduling instruction, try to extract and schedule
            if cal and ("scheduled" in cal.lower() or "schedule" in cal.lower()) and "http" not in cal:
                # Try to extract ISO date/time
                match = re.search(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})", cal)
                if match:
                    start_time = match.group(1)
                    # Use the rest as summary
                    summary = re.sub(r".*for \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*", "", cal)
                    if not summary.strip():
                        summary = cal.split("for")[0].strip()
                    # Actually schedule the event
                    cal_result = schedule_event(summary, start_time)
                    output["calendar"] = cal_result
            return output
        except Exception as e:
            raise Exception(f"Failed to process transcription with agent: {str(e)}") 