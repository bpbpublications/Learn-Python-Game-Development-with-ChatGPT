import openai
import pyttsx3
import speech_recognition as sr
from elevenlabs import generate, play
from elevenlabs import set_api_key
import nltk
from nltk.tokenize import PunktSentenceTokenizer

# Ensure that the Punkt tokenizer is downloaded
nltk.download('punkt')

elevenlabs = True
voices = { "MASTER" : "Bella",
          "<Miss Violet Purple>" : "Dorothy",
          "<Mister Jasper Teal>" : "Fin",
          "<Doctor Elliot Blue>" : "Patrick",
          }

if elevenlabs:
    set_api_key("")
else:
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    """VOLUME"""
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    print (volume)                          #printing current volume level
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

openai.api_key = ""

class StreamToVoice:
    def __init__(self, voices):
        self.tokenizer = PunktSentenceTokenizer()
        self.buffer = ""
        self.message = ""
        self.voices = voices

    def add_text(self, text):
        """
        Add text to the buffer and process it to detect complete sentences.
        :param text: str - A chunk of text to be added to the buffer.
        """
        self.buffer += text
        self.message += text
        sentences = self.tokenizer.tokenize(self.buffer)

        # Check if the last character is a sentence terminator
        if sentences and self.buffer[-1] in ['.', '?', '!']:
            for sentence in sentences:
                self.speak(sentence)
                print(sentence)
            self.buffer = ""  # Clear buffer after speaking
        else:
            # If the last piece of text didn't end with a sentence terminator, 
            # we assume it's not the end of the sentence yet and save the last
            # fragment back to the buffer.
            self.buffer = sentences[-1] if sentences else self.buffer

    def speak(self, text): 
        voice_name = None
        if elevenlabs:
            for k, v in self.voices.items():
                if k in text: 
                    voice_name = v
                    break
            if voice_name is None:
                voice_name = self.voices["MASTER"]
            audio = generate(
                text=text,
                voice=voice_name,
                model="eleven_multilingual_v2",        
                )

            play(audio)  
        else:
            engine.say(text)
            engine.runAndWait()
            
        
    def get_clear_message(self):
        msg = self.message
        self.buffer = ""
        self.message = ""
        return msg       


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.75
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print("====================================================================================================================================================================================")
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")  
        return "None"
    return query
    
    
messages = []

def load_text_from_file(file_path):    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print("The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

system_message = load_text_from_file('the_detective.txt')

messages.append({"role": "system", "content": system_message})
mess = "greet me"
messages.append({"role": "user", "content": mess})
response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages)
reply = response["choices"][0]["message"]["content"]
messages.append({"role": "assistant", "content": reply})

voice = StreamToVoice(voices)
voice.speak(reply)

while input != "quit()":
    message = takeCommand()
    if message == "goodbye":
        exit()
    
    messages.append({"role": "user", "content": message})
    response = openai.ChatCompletion.create(
        model="gpt-4",        
        messages=messages,
        stream=True,
        )
        
    message = []
    sentence = ""
    for chunk in response:
        try:
            text = chunk["choices"][0]["delta"]["content"]
            voice.add_text(text)
        except:
            break
    
    messages.append({"role": "assistant", "content": voice.get_clear_message()})
    
    