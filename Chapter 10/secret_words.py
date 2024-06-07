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
el_voice = "Bella"
secret_word = "gold"

if elevenlabs:
    set_api_key("77ead2055468a9978a7d91744bfc724a")
else:
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    """VOLUME"""
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    print (volume)                          #printing current volume level
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

openai.api_key = "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"

class StreamToVoice:
    def __init__(self):
        self.tokenizer = PunktSentenceTokenizer()
        self.buffer = ""
        self.message = ""

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
        if elevenlabs:
            audio = generate(
                text=text,
                voice=el_voice,
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
system_message = f"""
You are a game master that controls a secret word the players must guess by asking you questions.
Never reveal the secret word, but you can give hints to what the word is.
Ask the players if they want to start the game.
The game rules are:
1. Never reveal the secret word.
2. Players can only ask one question at a time.
3. Players may only ask 5 questions.
4. When player has asked all the 5 questions the game is over.
5. When the player guesses the secret word tell them they have won.
The secret word is {secret_word}
"""
messages.append({"role": "system", "content": system_message})
mess = "greet me"
messages.append({"role": "user", "content": mess})
response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages)
reply = response["choices"][0]["message"]["content"]
messages.append({"role": "assistant", "content": reply})

voice = StreamToVoice()
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
    #reply = response["choices"][0]["message"]["content"]
    
    message = []
    sentence = ""
    for chunk in response:
        try:
            text = chunk["choices"][0]["delta"]["content"]
            voice.add_text(text)
        except:
            break
    
    messages.append({"role": "assistant", "content": voice.get_clear_message()})
    
    