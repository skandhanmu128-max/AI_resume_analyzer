import os
import tempfile
from gtts import gTTS

def text_to_speech(text: str) -> str:
    """
    Converts text to speech and saves it to a temporary MP3 file.
    Returns the path to the MP3 file.
    """
    if not text:
        return ""
    
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Create a temp file that Streamlit can read
        fd, temp_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)
        
        tts.save(temp_path)
        return temp_path
    except Exception as e:
        print(f"TTS Error: {e}")
        return ""
