import speech_recognition as sr
from openai import OpenAI
from io import BytesIO

client = OpenAI(api_key="")


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.75
        audio = r.listen(source)

    audio_bytes = BytesIO(audio.get_wav_data())
    try:
        print("Recognizing...")
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_bytes, 
            response_format="text"
        )
        print(f"User said: {transcript}\n")
    except Exception as e:
        print("Say that again please...")
        print("Error:", e)  # To see what the actual error is
        return "None"
    
    return transcript 

text = ""

while "quit" not in text:
    text = listen()
    print(text)