import numpy as np
from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition, TransitionBase
from kivymd.app import MDApp
import json
import urlrequest
from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView
import time
import random
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy_garden.mapview import MapView
from kivy.core.window import Window
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.picker import MDTimePicker
from datetime import datetime
import requests
import urllib.parse
import geocoder
import sounddevice as sd
from scipy.io.wavfile import write
from kivy.uix.slider import Slider
from playsound import playsound
import simpleaudio as sa
from kivy.core.audio import SoundLoader
import base64
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.clock import mainthread

Window.size = (300, 533)

fs = 4410  # Sample rate
duration = 10  # Duration of recording
firstEnter = True
Time = ''
Date = ''

class FirstScreen(Screen):
    pass
class SearchLyricsScreen(Screen):
    getRecent = StringProperty()
    
    def on_enter(self):
        Clock.schedule_once(self.dispRecents)
    def dispRecents(self,dt):
        print('in search lyrics screen')    
        url = "https://zacapelt.pythonanywhere.com/recentSongs" #url the request is going to 
        response = urlrequest.sendurlrequest(url,{})
        dictOfResults = json.loads(response)
        print(dictOfResults)
        '''global firstEnter
        if firstEnter == True:
            for i in range(3):
                firstEnter = False
                button = Button(text = dictOfResults[i]['title'], on_press=self.press_auth)
                button.my_id = i
                self.ids.grid.add_widget(button)'''
        self.ids.grid.clear_widgets()
        for i in range(3):
            button = Button(text = dictOfResults[i]['title'], on_press=self.press_auth)
            button.my_id = i
            self.ids.grid.add_widget(button)
        #for i in range(3):
        #    self.ids.grid.remove_widget(self.ids.i)
    def press_auth(self, instance):
        url = "https://zacapelt.pythonanywhere.com/recentSongs" #url the request is going to 
        response = urlrequest.sendurlrequest(url,{})
        dictOfResults = json.loads(response)
        songDetails = {"song":dictOfResults[instance.my_id]['title'],"artist":dictOfResults[instance.my_id]['artist']}
        url = "https://zacapelt.pythonanywhere.com/getlyricsplus"
        response = urlrequest.sendurlrequest(url, songDetails) #sends a POST request to the Flask Webserver
        dictOfResults = json.loads(response) #converts the data to a python dictionary
        global lyrics
        lyrics = dictOfResults['lyrics']
        self.manager.current = 'displayLyricsPage'


class StartScreen(Screen):
    pass
class EventRego(Screen):
    def on_save(self, instance, value, date_range):
        #print(instance, value, date_range)
        self.ids.date_button.text = str(value)
        global Date
        Date = str(value)
    def on_cancel(self, instance, value):
        pass
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
    
    def get_time(self, instance,time):
        self.ids.time_button.text = str(time)
        global Time
        Time = str(time)
    def on_cancel(self,instance,time):
        pass
    def show_time_picker(self):
        default_time = datetime.strptime("7:00:00", '%H:%M:%S').time()
        time_dialog = MDTimePicker()
        time_dialog.set_time(default_time)
        time_dialog.bind(on_cancel=self.on_cancel, time=self.get_time)
        time_dialog.open()

class displayLyricsScreen(Screen,BoxLayout):
    getLyrics = StringProperty()
    def on_enter(self):
        Clock.schedule_once(self.dispLyrics)
    def dispLyrics(self,dt):    
        self.ids.lyricsLable.text = lyrics

class RecordAudio(Screen):
    pass


class MyScreenManager(ScreenManager):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return
    

    def getLogin(self):
        FirstScreen_instance = self.get_screen('loginPage')
        password = FirstScreen_instance.ids["password"].text
        username = FirstScreen_instance.ids["username"].text
        print(username, password)
        loginDetails = {"email":username,"password":password} #creates a dict of login details
        url = "https://zacapelt.pythonanywhere.com/login" #url the request is going to 
        response = urlrequest.sendurlrequest(url, loginDetails) #sends a POST request to the Flask Webserver
        dictOfResults = json.loads(response) #converts the data to a python dictionary
        print(dictOfResults)
        if dictOfResults['success']:
            self.current = 'start'
    
    def getRegistration(self):
        print("registration time!")
        FirstScreen_instance = self.get_screen('loginPage')
        password = FirstScreen_instance.ids["password"].text
        username = FirstScreen_instance.ids["username"].text
        print(username, password)
        registerDetails = {"email":username,"password":password} #creates a dict of login details
        url = "https://zacapelt.pythonanywhere.com/register" #url the request is going to 
        response = urlrequest.sendurlrequest(url, registerDetails) #sends a POST request to the Flask Webserver
        dictOfResults = json.loads(response) #converts the data to a python dictionary
        print(dictOfResults)
    
    def getLyrics(self):
        SearchLyricsScreen_instance = self.get_screen('SearchLyricsPage')
        songTitle = SearchLyricsScreen_instance.ids["songTitle"].text
        songArtist = SearchLyricsScreen_instance.ids["artist"].text
        print(songTitle)
        print(songArtist)
        songDetails = {"song":songTitle,"artist":songArtist}
        url = "https://zacapelt.pythonanywhere.com/getlyricsplus"
        response = urlrequest.sendurlrequest(url, songDetails) #sends a POST request to the Flask Webserver
        dictOfResults = json.loads(response) #converts the data to a python dictionary
        #print(dictOfResults)
        global lyrics
        lyrics = dictOfResults['lyrics']
        #print(lyrics)
        self.current = 'displayLyricsPage'
        return lyrics
    
    def getEventRegistration(self):
        EventRego_instance = self.get_screen('EventRego')
        address = EventRego_instance.ids["address"].text
        city = EventRego_instance.ids["city"].text
        postcode = EventRego_instance.ids["postcode"].text
        description = EventRego_instance.ids["description"].text
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
        response = requests.get(url).json()
        latitude = response[0]["lat"]
        longitude = response[0]["lon"]

        print(address,city,postcode,description,Time,Date,latitude,longitude)

        eventRegisterDetails = {"address":address,"city":city,"postcode":postcode,"description":description,"time":Time,"date":Date,"latitude":latitude,"longitude":longitude} #creates a dict of login details
        url = "https://zacapelt.pythonanywhere.com/eventRegister" #url the request is going to 
        response = urlrequest.sendurlrequest(url, eventRegisterDetails) #sends a POST request to the Flask Webserver
        dictOfResults = json.loads(response) #converts the data to a python dictionary
        print(dictOfResults)
    
    def sliderValue(self, value):
        #print(value)
        global duration
        duration = value

    def recordAudio(self):
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        write('output.wav', fs, myrecording)  # Save as WAV file
    
    def playAudio(self):
        #playsound('output.wav')
        sound = SoundLoader.load('output.wav')
        if sound:
            print("Sound found at %s" % sound.source)
            print("Sound is %.3f seconds" % sound.length)
            sound.play()
    
    def uploadAudio(self):
        audio_instance = self.get_screen('recordAudio')
        with open("output.wav", "rb") as audio_file:
            encoded_string = base64.b64encode(audio_file.read())
        description = audio_instance.ids["descriptionOfAudio"].text
        audioInformation = {"description":description,"audio":encoded_string}
        url = "https://zacapelt.pythonanywhere.com/audio" #url the request is going to 
        response = urlrequest.sendurlrequest(url, audioInformation) #sends a POST request to the Flask Webserver
        dictOfResults = json.loads(response) #converts the data to a python dictionary
        print(dictOfResults)
    
    def getRecent():
        print('in get recent')
        
    

    
root_widget = Builder.load_file("styleApp.kv")



class ScreenManagerApp(MDApp):
    def build(self):
        #print(geocoder.ip('me').latlng)
        return root_widget

ScreenManagerApp().run()