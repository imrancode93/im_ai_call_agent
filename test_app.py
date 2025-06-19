import unittest
import os
from transcriber import transcribe_audio
from agent import SalesCallAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TestSalesCallAssistant(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.test_audio_path = "samples/test_sales_call.mp3"
        self.agent = SalesCallAgent()

    def test_transcription(self):
        """Test audio transcription"""
        if not os.path.exists(self.test_audio_path):
            self.skipTest("Test audio file not found")
        
        transcription = transcribe_audio(self.test_audio_path)
        self.assertIsNotNone(transcription)
        self.assertIsInstance(transcription, str)
        self.assertTrue(len(transcription) > 0)

    def test_agent_analysis(self):
        """Test agent's analysis of transcription"""
        test_transcription = """
        Hello, this is John from TechSolutions. I'm calling to follow up on our previous discussion 
        about your company's IT infrastructure needs. We discussed upgrading your current system 
        to improve efficiency and security.
        """
        
        summary, action_items = self.agent.process_transcription(test_transcription)
        
        self.assertIsNotNone(summary)
        self.assertIsInstance(summary, str)
        self.assertTrue(len(summary) > 0)
        
        self.assertIsNotNone(action_items)
        self.assertIsInstance(action_items, list)
        self.assertTrue(len(action_items) > 0)

    def test_environment_variables(self):
        """Test environment variables are set"""
        self.assertIsNotNone(os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not set")

if __name__ == '__main__':
    unittest.main() 