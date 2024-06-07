import pyttsx3

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

tts_os(text)

