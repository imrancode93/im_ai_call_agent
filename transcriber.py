import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def transcribe_audio(audio_file_path):
    """
    Transcribe audio file using OpenAI's Whisper API (OpenAI Python 1.x+).
    
    Args:
        audio_file_path (str): Path to the audio file
        
    Returns:
        str: Transcribed text
    """
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Open the audio file
        with open(audio_file_path, "rb") as audio_file:
            # Create transcription
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
        
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}") 