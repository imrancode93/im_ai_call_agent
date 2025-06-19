# AI Sales Call Assistant

An AI-powered tool that automatically transcribes sales calls, generates summaries, and identifies action items using OpenAI's Whisper and GPT-4.

## Features

- 🎙️ Audio transcription using OpenAI Whisper
- 📊 AI-powered call analysis and summarization
- ✅ Automatic action item extraction
- 🌐 Real-time web search via SerpAPI
- 📅 Google Calendar integration for scheduling meetings
- 🎯 Clean Streamlit interface
- 🐳 Dockerized for easy deployment

## Prerequisites

- Python 3.10 or higher
- OpenAI API key
- SerpAPI key (for web search)
- Google Cloud project with Calendar API enabled
- Docker (for containerized deployment)

## Local Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-sales-call-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```
Edit `.env` and add your OpenAI API key, SerpAPI key, and any other required variables.

5. Run the application:
```bash
streamlit run app.py
```

## Advanced Features & Integrations

### Google Calendar Integration

- **Setup:**
  1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials) and create OAuth 2.0 credentials.
  2. Download the credentials file and save as `credentials.json` in your project root.
  3. Add `http://localhost:8080/` as an authorized redirect URI.
  4. Add your Google account as a test user in the OAuth consent screen.
  5. Run the authentication script:
     ```bash
     python google_auth_setup.py
     ```
     - This will open a browser for you to log in and authorize access.
     - After successful login, a `token.json` file will be created.

- **Usage:**
  - The agent can schedule meetings directly in your Google Calendar when the call mentions scheduling a demo or follow-up.
  - The UI will show a clickable link to the created event.

### Web Search (SerpAPI)
- Add your SerpAPI key to `.env` as `SERPAPI_API_KEY`.
- The agent will use real-time web search to find competitor/product information when relevant.
- Results are shown as clickable links in the UI.

## Docker Deployment

### Local Docker

1. Build the Docker image:
```bash
docker build -t ai-sales-call-assistant .
```

2. Run the container:
```bash
docker run -p 8501:8501 --env-file .env ai-sales-call-assistant
```

### Deploying to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the service:
   - Build Command: `docker build -t ai-sales-call-assistant .`
   - Start Command: `docker run -p 8501:8501 --env-file .env ai-sales-call-assistant`
4. Add environment variables in Render's dashboard
5. Deploy!

### Deploying to AWS EC2

1. Launch an EC2 instance (t2.micro or larger recommended)
2. Install Docker on the instance:
```bash
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
```

3. Clone the repository and build the Docker image:
```bash
git clone <repository-url>
cd ai-sales-call-assistant
docker build -t ai-sales-call-assistant .
```

4. Run the container:
```bash
docker run -d -p 8501:8501 --env-file .env ai-sales-call-assistant
```

5. Configure security group to allow inbound traffic on port 8501

## Usage

1. Open the application in your browser (default: http://localhost:8501)
2. Upload an MP3 file of your sales call
3. Wait for the transcription and analysis to complete
4. Review the transcription, summary, action items, calendar events, and web search results

## Advanced UI & Agent Notes

- **Action Items:** Displayed as a checklist for easy tracking.
- **Calendar Events:** Created directly in your Google Calendar with a clickable link in the UI.
- **Web Search Results:** Shown as a list of clickable links with titles.
- **Agent:** Uses LangChain with OpenAI and tool integrations. The agent is prompted to always include web search results in the output if the tool is used.

## Troubleshooting & Notes

- **Google Calendar: redirect_uri_mismatch**
  - Add `http://localhost:8080/` to your OAuth credentials in Google Cloud Console.
  - Add your Google account as a test user in the OAuth consent screen.
- **Google Calendar: access_denied**
  - Your app must be in test mode and your account must be a test user.
- **Web Search Results Not Showing**
  - The agent prompt now enforces inclusion of web search results in the output.
- **Proxies Error with OpenAI**
  - Use the latest versions of `langchain`, `langchain-openai`, and `openai` as specified in `requirements.txt`.
- **Event Not Created in Calendar**
  - The agent now actually calls the scheduling function, not just outputs a summary string.
- **Sample Audio Generation**
  - Use `create_test_audio.py` to generate a sample call that triggers both web search and calendar tools.

## Security Notes

- Never commit your `.env` file or expose your API keys
- Use environment variables for sensitive information
- Consider implementing user authentication for production use

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 