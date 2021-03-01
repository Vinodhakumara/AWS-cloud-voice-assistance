import pyttsx3 as txt  # Speak 
import speech_recognition as sr # Recognize
converter = ""
converter = txt.init() # Initialize the converter 
converter.setProperty('rate', 140)  # Can be more than 100 # Sets speed percent 
converter.setProperty('volume', 1) #To Change a Voice # Set volume 0-1 
voices = converter.getProperty('voices')
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

def change_voice(): # Use female voice  #converter.setProperty('voice', voice_id) 
    if voices[1].id == True:
        converter.setProperty('voice', voices[1].id)
    else:
        converter.setProperty('voice', voices[0].id)
        
def inc_vol(): #Increase Volume
    converter.setProperty('volume', 1)   

def dec_vol():  #Decrease Volume
    converter.setProperty('volume', 0.1) 
    
def speak_fast(): #Speak Fast
    converter.setProperty('rate', 180)
    
def speak_slow(): #Speak Slow
    converter.setProperty('rate', 100)
    
def save_file(file='test.mp3'):  #Save my words to a mp3 file
    converter.save_to_file(listen() , file)
    converter.runAndWait()
    
def speak(speaks): #Speak 
    converter.setProperty('voice', voices[1].id)
    converter.say(speaks)
    converter.runAndWait()

def listen():  # Listens and Converts to text
    r = sr.Recognizer()    # Load Recognizer
    with sr.Microphone() as source:
        speak("Start Saying..")
        audio = r.listen(source)
        speak("Got it please wait...")
    voice_txt = r.recognize_google(audio)
    return voice_txt

def changeLang(data,lang = "kn"): # Convert from English words to other language words
    if data != "":
        with sr.Microphone() as source:
                print("start say...")
                data = r.listen(source)
                print("speaking done....")
    LangConv = r.recognize_google(data,language = lang)
    return LangConv