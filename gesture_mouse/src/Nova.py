import pyttsx3
import speech_recognition as sr
from datetime import date
import time # this is my branch
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import pyjokes
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import Gesture_Controller
import app
from threading import Thread
from constants.constants import *


# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# engine.setProperty('rate', 150)
# engine.setProperty('volume', 0.7)
engine.setProperty('voice', voices[0].id)

# ----------------Variables------------------------
file_exp_status = False
files =[]
path = ''
is_awake = True  #Bot status

# ------------------Functions----------------------
def reply(audio):
    app.ChatBot.addAppMsg(audio)
    print(audio)
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        reply("Good Morning!")
    elif hour>=12 and hour<18:
        reply("Good Afternoon!")   
    else:
        reply("Good Evening!")  
        
    reply("I am Nova, how may I help you?")

# Set Microphone parameters
with sr.Microphone() as source:   
       r.energy_threshold = 500 
       r.dynamic_energy_threshold = False

# Audio to String (change)
def record_audio():
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        voice_data = ''
        audio = r.listen(source, phrase_time_limit=5)

        try:
            voice_data = r.recognize_google(audio)
        except sr.RequestError:
            reply('Sorry my Service is down. Plz check your Internet connection')
        except sr.UnknownValueError:
            print('cant recognize')
            pass
        return voice_data.lower()


# Executes Commands (input: string)
def respond(voice_data):
    global file_exp_status, files, is_awake, path
    voice_data.replace('nova','')
    if voice_data != None and voice_data != "" :
         app.eel.addUserMsg(voice_data)
    if is_awake==False:
        if 'wake up' in voice_data:
            is_awake = True
            wish()

    # STATIC CONTROL
    elif 'hello' in voice_data:
        wish()

    elif 'what is your name' in voice_data:
        reply('My name is Nova!')
        
    
    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])
    
    elif 'search' in voice_data:
        reply('Searching for ' + voice_data.split('search')[1])
        url = 'https://google.com/search?q=' + voice_data.split('search')[1]
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')
            
    elif 'open' in voice_data:
        val  =voice_data.split('open')[1]
        val = val.strip().lower()
        reply('opening ' +val )
        url = 'https://'+val+'.com'
        try:
            webbrowser.get().open(url)
            reply('Opened '+val)
        except:
            reply('Please check your Internet')

    elif 'location' in voice_data:
        reply('Which place are you looking for ?')
        temp_audio = record_audio()
        app.eel.addUserMsg(temp_audio)
        reply('Locating...')
        url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')

    elif ('bye' in voice_data) or ('by' in voice_data):
        reply("Good bye! Have a nice day.")
        is_awake = False

    elif ('exit' in voice_data) or ('terminate' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
        app.ChatBot.close()
        sys.exit()
        
    
    # DYNAMIC CONTROLS
    elif 'launch gesture recognition' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            reply('Gesture recognition is already active')
        else:
            gc = Gesture_Controller.GestureController()
            t = Thread(target = gc.start)
            t.start()
            reply('Launched Successfully')

    elif 'stop gesture recognition' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
            reply('Gesture recognition Stopped')
        else:
            reply('Gesture recognition is already inactive')
        
    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')
          
    elif 'page' in voice_data or 'pest'  in voice_data or 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')
        
    # File Navigation (Default Folder set to C://)
    elif 'list' in voice_data:
        counter = 0
        path = 'C://'
        files = listdir(path)
        filestr = ""
        for f in files:
            counter+=1
            print(str(counter) + ':  ' + f)
            filestr += str(counter) + ':  ' + f + '<br>'
        file_exp_status = True
        reply('These are the files in your root directory')
        app.ChatBot.addAppMsg(filestr)
        
    elif file_exp_status == True:
        counter = 0   
        if 'open' in voice_data:
            if isfile(join(path,files[int(voice_data.split(' ')[-1])-1])):
                os.startfile(path + files[int(voice_data.split(' ')[-1])-1])
                file_exp_status = False
            else:
                try:
                    path = path + files[int(voice_data.split(' ')[-1])-1] + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter+=1
                        filestr += str(counter) + ':  ' + f + '<br>'
                        print(str(counter) + ':  ' + f)
                    reply('Opened Successfully')
                    app.ChatBot.addAppMsg(filestr)
                    
                except:
                    reply('You do not have permission to access this folder')
                                    
        if 'back' in voice_data:
            filestr = ""
            if path == 'C://':
                reply('Sorry, this is the root directory')
            else:
                a = path.split('//')[:-2]
                path = '//'.join(a)
                path += '//'
                files = listdir(path)
                for f in files:
                    counter+=1
                    filestr += str(counter) + ':  ' + f + '<br>'
                    print(str(counter) + ':  ' + f)
                reply('ok')
                app.ChatBot.addAppMsg(filestr)
    # elif ("google" in voice_data) or ("search" in voice_data) or ("web browser" in voice_data) or ("chrome" in voice_data) or ("browser" in voice_data):
    #     pyttsx3.speak("Opening")
    #     pyttsx3.speak("GOOGLE CHROME")
    #     print(".")
    #     print(".")
    #     os.system("chrome")
 
    # elif ("start ie" in voice_data) or ("start msedge" in voice_data) or ("start edge" in voice_data):
    #     pyttsx3.speak("Opening")
    #     pyttsx3.speak("MICROSOFT EDGE")
    #     print(".")
    #     print(".")
    #     os.system("msedge")
 
    # elif ("start mote" in voice_data) or ("start notes" in voice_data) or ("start notepad" in voice_data):
    #     pyttsx3.speak("Opening")
    #     pyttsx3.speak("NOTEPAD")
    #     print(".")
    #     print(".")
    #     os.system("Notepad")
 
    # elif ("start visual studio code" in voice_data) or ("start studio code" in voice_data) or ("start visual code" in voice_data) or ("start visual studio code" in voice_data):
    #     pyttsx3.speak("Opening")
    #     pyttsx3.speak("Visual studio code")
    #     print(".")
    #     print(".")
    #     os.system("Visual Studio Code")
 
    # elif ("start android studio" in voice_data):
    #     pyttsx3.speak("Opening")
    #     pyttsx3.speak("Android studio")
    #     print(".")
    #     print(".")
    #     os.system("Android Studio")
 
    # elif "start slack" in voice_data :
    #     pyttsx3.speak("Opening")
    #     pyttsx3.speak("Slack")
    #     os.system("Slack")

    elif 'how are you' in voice_data:
            reply("I am fine, Thank you")
            reply("How are you, Sir")
            
    elif "good morning" in voice_data:
            reply("A warm good morning")
            reply("How are you")
            
    elif 'fine' in voice_data or "good" in voice_data:
            reply("It's good to know that your fine")
             
    elif "who made you" in voice_data or "who created you" in voice_data:
            reply("I have been created by Team major including Gaurav Divya and Chaitra")
            
    elif 'joke' in voice_data:
           reply(pyjokes.get_joke())
           
    elif "who are you" in voice_data:
           reply("I am your virtual assistant created by my team")
           
    elif 'reason for you' in voice_data:
           reply("I was created  to help you")
           
    # elif "where is" in voice_data:
    #        voice_data = voice_data.replace("where is", "")
           
    #        reply("User asked to Locate"+location)
    #        webbrowser.open("https://www.google.nl/maps/place/"+location)
 
    elif "i love you" in voice_data:
           reply("I already have a girlfriend")
           
    elif "wikipedia" in voice_data:
            webbrowser.open("wikipedia.com")      

    elif 'news' in voice_data or 'headlines' in voice_data :
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            reply('Here are some headlines from the Times of India,Happy reading')
            time.sleep(6)

    elif "log off" in voice_data or "sign out" in voice_data:
            reply("Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])
    
    elif "weather" in voice_data:
            api_key="8ef61edcf1c576d65d836254e11ea420"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            reply("whats the city name")
            city_name=record_audio()
            respond(city_name)
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                reply(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

    elif 'location' in voice_data:
        reply('Which place are you looking for ?')
        temp_audio = record_audio()
        app.eel.addUserMsg(temp_audio)
        reply('Locating...')
        url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')

    
    else: 
        if master_control and voice_data == "":
            pass
        else :
            reply('I am not functioned to do this !')

# ------------------Driver Code--------------------
    
   


t1 = Thread(target = app.ChatBot.start)
t1.start()
while not app.ChatBot.started:
    time.sleep(0.5)
wish()
voice_data = None
master_control = False

while True:
    if app.ChatBot.isUserInput():
        voice_data = app.ChatBot.popUserInput()
    else:
        voice_data = record_audio()
        print(voice_data)
    if any(value in voice_data for value in NOVA) or master_control:  
        if MASTER_CONTROL in voice_data and DEACTIVATE in voice_data :
             master_control = False
             reply("Master control deactivated")
        elif MASTER_CONTROL in voice_data and ACTIVATE in voice_data :
             master_control = True
             reply("Master control activated")     
        else : 
            try:
                respond(voice_data)
            except SystemExit:
                reply("Exit Successfull")
                break
            except:
                print("EXCEPTION raised while closing.") 
                break
        


