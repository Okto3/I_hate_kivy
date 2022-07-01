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

Window.size = (300, 533)


Time = ''
Date = ''

class FirstScreen(Screen):
    pass
class SearchLyricsScreen(Screen):
    pass
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
    

    
root_widget = Builder.load_file("styleApp.kv")



class ScreenManagerApp(MDApp):
    def build(self):
        print(geocoder.ip('me').latlng)
        return root_widget

ScreenManagerApp().run()