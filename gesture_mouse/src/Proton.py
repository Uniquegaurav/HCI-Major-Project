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
 

    elif "what is your favourite bird" in voice_data:
            reply("my favorite bird is peacock, which is India's national bird")


    elif "which is ur favorite quote" in voice_data:
            reply("my favorite quote is a good book is like hundred good friends ,but a good friend is like a library")
 
    elif "who is the most popular althlete in India" in voice_data:
            reply("virat kohli is the most popular althlete in india, he is an Indian cricketer ")

    elif "what is best peice of advice for students" in voice_data:
            reply(" the best peice of advice for students wil be Dreams remain dreams until you take action.")

    elif "how many days in a week" in voice_data:
            reply("one week hold for 7 days")

    elif "which laptop is best for students" in voice_data:
            reply("dell laptops are recoginzed as best laptops for students, its powreded by an 11th Gen Intel core i7 processor.")

    elif "what is most popular sport in india " in voice_data:
            reply("cricket has been most popular sport in inida, the country has hosted and won the cricket world cup on mutiple occasions.")

    elif "what is the  best principle to follow in life" in voice_data:
            reply("here the information from thrirdcalotogue -1.attitude is everything 2. be of service to others ") 

    elif "who is the most popular actor in india" in voice_data:
            reply("here is the information from javatpoint Shah rukh khan ,he is the most popluar actor in india")

    elif "who is the most popular soccer player in world" in voice_data:
            reply(" the most popular soccer players are cristiano ronaldo, lionel messi, neymar jr.")

    elif "what is popluar cuisine" in voice_data:
            reply("italian food is officially the most popluar cusine in world, an international yougov study asked more than 25,000 people across 24 countires.")

    elif "what is the most likely subject for students" in voice_data:
            reply("mathematics was the most popluar subject overall , selected by 38% of worldwide in the analyisis given by cambrigde university")

    elif "what is your team mates name " in voice_data:
            reply("they are gaurav,chaitra,divya")

    elif "who is the PM of india " in voice_data:
            reply("according to wikkipedia, narendra modi is the prime minister of india,who is head of government of republic of india")

    elif "what is the value of pi" in voice_data:
            reply("the value of pi is 3.142")

    elif "what the benefits of using social media" in voice_data:
            reply(" accoridng to survey , social media also helps you to build your brand because it enables sharing")

    elif "what is the most popular pizza in the world" in voice_data:
            reply(" in a poll of more than 6000 US adults,americas favorite pizza topping is pepperoni")

    elif "whats the color of sky" in voice_data:
            reply(" the earth atmosphere scatter sunlight in all directions ,blue light scatter more , this is why we see a blue sky most of time")

    elif "which is the most used gadgets in india" in voice_data:
            reply("one plus, is a chinese consumer electronics manufactured headquartereted in shenzhen")

    elif "what is big bang theory" in voice_data:
            reply("according to the survey by nasa , bigbang is how astronomers explain the way the universe began")

    elif "does universe have center" in voice_data:
            reply("ever since the big bang 13.7 billion years ago, no matter how we try to define and identify ,universe has no center.")

    elif "which is the most popluar country in the world" in voice_data:
            reply("according to survey by novit france is the most popular country in the world")

    elif "what is the color of mirror" in voice_data:
            reply("according to bbc magezine survey as a perfect mirror reflects back all the colours comprising white light, its also white. ")
            
    elif "how much of our brain do we use? " in voice_data:
            reply("according to pinterest studies from 65% 0f americans belive that we only use 10% of our brain,but this is just a myth.")   

    elif "which is the most expensive flower in the world" in voice_data:
            reply("according to wikipedia, shenzhen nongke orchid is most expensive flower in the world")
                
    elif "what is the resolution of the human eye?" in voice_data:
            reply("576 megapixiles is the resolution of human eye,the digital images are made of millions of tiny tiles-like elements accoring to survey.")
            
    elif "which came first - the egg or the chicken?" in voice_data:
            reply("according to the dovit survey, the egg-laying animals existed way far before the chicken came , so techincally the egg came before the chicken")
            
    elif "can you fire a gun in space" in voice_data:
            reply("guns dont require oxygen to work, so vaccum of outerspace will not be a problem, we can fire a gun in space")
            
    elif "how much money is there in the world" in voice_data:
            reply("well, its difficult to figure out the accurate number but this most accurated money is 75 trillion US dollars")
            
    elif "how much is the earth worth?" in voice_data:
            reply("according to greg loughman, the worth of earth is 3 to 4.4 quadrillion pounds")
            
    elif "is time travel really possible?" in voice_data:
            reply("based on the available theories ,we can travel in future,but still ,we dont know whether they are possible for real objects.")
            
    elif "how old are you" in voice_data:
            reply(" i was launched in 2021, so im fairly young, but i learned so much i hope im wise beyond my years")
            
    elif "where is Georgia" in voice_data:
            reply("according to wikipedia ,Georgia is a state in southastern region of united ststes ,borderd to north by tennessee and north carolina")
            
    elif "which is smartest mammal" in voice_data:
            reply(" based on current metrices for intelligence, dolphins are one of the most intelligent animals in world")
            
    elif "which is the fastest animal in the world" in voice_data:
            reply("according to wikkipedia, cheetah is capable of going from 0 to 60 miles per hr in less than three seconds, cheetah is considered the fatest land animal in the world")
            
    elif "how many continents in the world" in voice_data:
            reply("here's the information from worldmeta, there are 7 continents in the world, adn asia is the biggest continent")
            
    elif "which is the best pet for humans" in voice_data:
            reply("here is the information from petscry , accordingly dogs and cats are considered to be best pet for humans")
            
    elif "how much water should be consumed by human in a day" in voice_data:
            reply("according to us, national academics of science , it was determined that an adequate daily fluid intake is about 15.5 cups of fluids a day")
			             
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
        


