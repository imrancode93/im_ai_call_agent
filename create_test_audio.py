from gtts import gTTS
import os

def create_test_audio():
    """
    Create a test sales call audio file using text-to-speech.
    """
    # Sample sales conversation
    text = """
    Hello, this is Sarah from TechSolutions. I wanted to follow up on our previous conversation about upgrading your company's cloud infrastructure.

    We've recently launched a new cloud-based platform that can help reduce your operational costs by up to 30%. I noticed that Acme Corp just released their own cloud solution last week, and I thought it would be helpful to compare their features and pricing to ours. Could you look up the latest reviews and comparisons between TechSolutions and Acme Corp's cloud products?

    Also, I'd like to schedule a demo to walk you through our platform and answer any questions you might have. Let's set up a meeting for 2025-07-02T15:00:00. Please add this to your calendar.

    Thank you, and I look forward to speaking with you soon!
    """
    
    # Create samples directory if it doesn't exist
    if not os.path.exists("samples"):
        os.makedirs("samples")
    
    # Generate speech
    tts = gTTS(text=text, lang='en', slow=False)
    
    # Save the file
    file_path = os.path.join("samples", "test_sales_call.mp3")
    tts.save(file_path)
    print(f"Test audio file created at: {file_path}")
    return file_path

if __name__ == "__main__":
    create_test_audio() 