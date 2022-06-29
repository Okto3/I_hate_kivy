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


lyrics = ""
songTitle = ""
songArtist = ""

class FirstScreen(Screen):
    pass
class SearchLyricsScreen(Screen):
    pass
class StartScreen(Screen):
    def mapView(self):
        mapview = MapView(zoom=12, lat=55.6712674, lon=12.5938239)
class EventRego(Screen):
    pass
class displayLyricsScreen(Screen,BoxLayout):
    getLyrics = StringProperty()
    message = StringProperty()
    btn = ObjectProperty(None)

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
         
    

    

root_widget = Builder.load_file("styleApp.kv")



class ScreenManagerApp(App):
    def build(self):
        return root_widget

ScreenManagerApp().run()