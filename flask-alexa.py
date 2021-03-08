# -*- coding: utf-8 -*-
"""
@author: Satyajit Pattnaik

"""

from flask import Flask,render_template,redirect,request
import warnings
warnings.filterwarnings('ignore')


import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import wikipedia
import sys
import requests, json 

listener = sr.Recognizer()
#engine = pyttsx3.init()

import os

app = Flask("__name__")

def engine_talk(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

    
def user_commands():
    try:
        with sr.Microphone() as source:
            print("Start Speaking!!")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            command = command.replace('alexa', '')
            if 'alexa' in command:
                print(command)
    except:
        pass
    return command

def weather(city):
    # Enter your API key here 
    api_key = "<YOUR API KEY>"
    #How to use api_key, see the below code:
    #api_key = "ABCDE"
    
    # base_url variable to store url 
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # Give city name 
    city_name = city
    
    # complete_url variable to store 
    # complete url address 
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
    
    # get method of requests module 
    # return response object 
    response = requests.get(complete_url) 
    
    # json method of response object  
    # convert json format data into 
    # python format data 
    x = response.json() 
    
    # Now x contains list of nested dictionaries 
    # Check the value of "cod" key is equal to 
    # "404", means city is found otherwise, 
    # city is not found 
    if x["cod"] != "404": 
    
        # store the value of "main" 
        # key in variable y 
        y = x["main"] 
    
        # store the value corresponding 
        # to the "temp" key of y 
        current_temperature = y["temp"] 
        temp_in_celcius = current_temperature - 273.15
        return str(int(temp_in_celcius))
    
    
def run_alexa():
    command = user_commands()
    if 'play a song' in command:
        song = 'Arijit Singh'
        engine_talk('Playing some music')
        print("Playing....")
        pywhatkit.playonyt(song)
    elif 'play' in command:
        song = command.replace('play', '')
        engine_talk('Playing....' + song)
        print("Playing....")
        pywhatkit.playonyt(song)     
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        engine_talk('Current Time is' + time)
    elif 'joke' in command:
        get_j = pyjokes.get_joke()
        print(get_j)
        engine_talk(get_j)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        engine_talk(info)
    elif 'weather' in command:
        #engine_talk('Please tell name of the city')
        city = 'Hong Kong'
        #city = 'Mumbai'
        engine_talk('The temperature in Hong Kong is' + weather(city) + 'degree celcius')
    elif 'stop' in command:
        engine_talk("Good bye")
    else:
        engine_talk("I didn't hear you properly")
        print("I didn't hear you properly")


@app.route('/')
def hello():
    return render_template("alexa.html")

@app.route("/home")
def home():
    return redirect('/')

@app.route('/',methods=['POST', 'GET'])
def submit():
    while True:
        run_alexa()
    return render_template("alexa.html")
        

if __name__ =="__main__":
    app.run(debug=True)
