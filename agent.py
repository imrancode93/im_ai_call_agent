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
                3. If a meeting/demo/follow-up is mentioned or needed:
                   - ALWAYS use the Calendar tool to schedule it
                   - Format the date and time EXACTLY like this: 2025-06-26T14:00:00
                   - Include a clear summary of what the meeting is about
                   - Example Calendar tool usage: schedule_event("Sales Demo Follow-up", "2025-06-26T14:00:00")
                4. If a competitor, product, or market trend is mentioned, use the Web Search tool to find relevant info

                IMPORTANT CALENDAR INSTRUCTIONS:
                - If any meeting, demo, or follow-up is discussed, you MUST schedule it
                - Always use ISO 8601 format for dates (YYYY-MM-DDTHH:MM:SS)
                - The Calendar section of your response should only contain the result from the Calendar tool
                - Do not include any other text in the Calendar section

                IMPORTANT WEB SEARCH INSTRUCTIONS:
                - If you use the Web Search tool, include the search results in the 'Web Search' section
                - Format the 'Web Search' section as a list of links and short descriptions

                Return your results in this format:
                Executive Summary: ...
                Action Items: ...
                Calendar: ...
                Web Search: ...

                Here is the transcription:
                """ + transcription
            )
            result = self.agent.run(prompt)
            
            # Parse the result into sections
            output = {"summary": "", "action_items": [], "calendar": "", "web_search": ""}
            
            # Parse each section
            for section in ["Executive Summary", "Action Items", "Calendar", "Web Search"]:
                if section in result:
                    # Split by section and get the content
                    part = result.split(section + ":", 1)[1]
                    # Find the next section to get the boundary
                    next_section = [s for s in ["Executive Summary", "Action Items", "Calendar", "Web Search"] 
                                  if s != section and s+":" in part]
                    if next_section:
                        part = part.split(next_section[0] + ":", 1)[0]
                    part = part.strip()
                    
                    # Handle action items as a list
                    if section == "Action Items":
                        items = [item.strip("- ") for item in part.split("\n") if item.strip()]
                        output["action_items"] = items
                    else:
                        output[section.lower().replace(" ", "_")] = part

            # Additional calendar processing if needed
            cal_output = output.get("calendar", "")
            if cal_output and "Event created:" not in cal_output and "http" not in cal_output:
                # Try to extract date and summary
                date_match = re.search(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})", cal_output)
                if date_match:
                    start_time = date_match.group(1)
                    summary = cal_output.split(start_time)[0].strip()
                    if not summary:
                        summary = "Follow-up Meeting"
                    # Schedule the event
                    cal_result = schedule_event(summary, start_time)
                    output["calendar"] = cal_result

            return output
        except Exception as e:
            raise Exception(f"Failed to process transcription with agent: {str(e)}") 