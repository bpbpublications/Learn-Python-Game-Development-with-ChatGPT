import pyttsx3
from elevenlabs import voices, generate, play
from elevenlabs import set_api_key


text = "Hello there!!"

def tts_os(text):
    #standard text to speech
    engine = pyttsx3.init('sapi5')
    voices_ = engine.getProperty('voices')
    engine.setProperty('voice', voices_[0].id)
    
    volume = engine.getProperty('volume')   
    print (volume)                         
    engine.setProperty('volume',1.0)    

    engine.say(text)
    engine.runAndWait()


def tts_elevenlabs(text):
    #Eleven Labs text to speech
    set_api_key("your-api-key")

    voices_ = voices()
    audio = generate(text=text, voice=voices_[0])
    print(voices_)

    play(audio)
    

tts_os(text)

tts_elevenlabs(text)