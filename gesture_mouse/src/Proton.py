import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import pyjokes
import wolframalpha 
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
#import Gesture_Controller
#import Gesture_Controller_Gloved as Gesture_Controller
from selenium import webdriver # to control browser operations
import app
from threading import Thread


# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
engine = pyttsx3.init()
voices = engine.getProperty('voices')
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
        
    reply("I am Proton, how may I help you?")

# Set Microphone parameters
with sr.Microphone() as source:   
       r.energy_threshold = 500 
       r.dynamic_energy_threshold = False

# Audio to String
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
    print(voice_data)
    voice_data.replace('proton','')
    app.eel.addUserMsg(voice_data)

    if is_awake==False:
        if 'wake up' in voice_data:
            is_awake = True
            wish()

    # STATIC CONTROLS
    elif 'hello' in voice_data:
        wish()

    
    
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
        # if Gesture_Controller.GestureController.gc_mode:
        #     Gesture_Controller.GestureController.gc_mode = 0
        app.ChatBot.close()
        #sys.exit() always raises SystemExit, Handle it in main loop
        sys.exit()
        
    
    # DYNAMIC CONTROLS
    # elif 'launch gesture recognition' in voice_data:
    #     if Gesture_Controller.GestureController.gc_mode:
    #         reply('Gesture recognition is already active')
    #     else:
    #         gc = Gesture_Controller.GestureController()
    #         t = Thread(target = gc.start)
    #         t.start()
    #         reply('Launched Successfully')

    # elif 'stop gesture recognition' in voice_data:
    #     if Gesture_Controller.GestureController.gc_mode:
    #         Gesture_Controller.GestureController.gc_mode = 0
    #         reply('Gesture recognition Stopped')
    #     else:
    #         reply('Gesture recognition is already inactive')
        
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
           reply("Im not intrested ,thanks")
           
    elif "wikipedia" in voice_data:
            webbrowser.open("wikipedia.com")  

    elif 'what is your name' in voice_data:
        reply('My name is Proton!')

    elif 'how are you' in voice_data :
            reply("I am fine, Thank you")   
    
    
    elif 'what can you do for me' in voice_data:
          reply('I can play songs, tell time, and help you go with wikipedia')

    elif "calculate" in voice_data:
             
            app_id = "Wolframalpha api id"
            client = wolframalpha.Client(app_id)
            indx = voice_data.lower().split().index('calculate')
            voice_data = voice_data.split()[indx + 1:]
            res = client.voice_data(' '.join(voice_data))
            answer = next(res.results).text
            print("The answer is " + answer)
            reply("The answer is " + answer)
 

    elif 'whats your favorite color' in voice_data:
            reply("my favorite color is black")


    elif "which is ur favorite quote" in voice_data:
            reply("nothing is impossible to achieve.")
 
    elif "can we count stars in night" in voice_data:
            reply("no we cant count")

    elif "how many days in a year" in voice_data:
            reply(" we have 365 days in a year.")

    elif "how many days in a week" in voice_data:
            reply("7 days in a week")

    elif "which laptop is best for students" in voice_data:
            reply("hp is best for students")

    elif "what is your favorite sport" in voice_data:
            reply("football is my favorite sport")

    elif "what is the principle you follow in life" in voice_data:
            reply("Be kind stay grounded as much as possible") 

    elif "who is your favorite actress" in voice_data:
            reply("zendaya is my favorite actress")


    elif "which is your favorite team in IPL" in voice_data:
            reply(" its obvious RCB royal challengers banglore")

    elif "what is your favorite cuisines" in voice_data:
            reply("italian is my favorite")

    elif "what is favorite subject" in voice_data:
            reply("histroy is my favorite subject")

    elif "what is your team mates name " in voice_data:
            reply("they are gaurav,chaitra,divya")

    elif "who is the PM of india " in voice_data:
            reply("narendra modi is pm of india")

    elif "what is the value of pi" in voice_data:
            reply("3.14 is value of pi")

    elif "do you have any pets" in voice_data:
            reply(" i love dogs, i have dog, i hate cats")

    elif "do you like pizza" in voice_data:
            reply(" yes i love pizza")

    elif "do you belive in magic" in voice_data:
            reply(" yes i belive in magic")

    elif "who is founder on siddaganga mutt" in voice_data:
            reply(" sri haradanahalli gosala siddeshwara swami is founder of siddaganga mutt")

    elif "which is your favorite movie" in voice_data:
            reply(" hidden figures is my favorite movie")

    elif "what is your favorite fruit" in voice_data:
            reply("my favorite fruit is grapes")

    elif "which is largest country in world" in voice_data:
            reply("russia is largest country in world")
			             
			             
    else: 
        reply('I am not functioned to do this !')

    

# ------------------Driver Code--------------------

t1 = Thread(target = app.ChatBot.start)
t1.start()

# Lock main thread until Chatbot has started
while not app.ChatBot.started:
    time.sleep(0.5)

wish()
voice_data = None
while True:
    if app.ChatBot.isUserInput():
        #take input from GUI
        voice_data = app.ChatBot.popUserInput()
    else:
        #take input from Voice
        voice_data = record_audio()
        print(voice_data)
    #process voice_data
    print(voice_data)
    if 'proton' in voice_data:
        try:
            #Handle sys.exit()
            respond(voice_data)
        except SystemExit:
            reply("Exit Successfull")
            break
        except:
            #some other exception got raised
            print("EXCEPTION raised while closing.") 
            break
        


