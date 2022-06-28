import numpy as np
from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivymd.app import MDApp
import json
import urlrequest
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
import time
import random
from kivy.properties import StringProperty, ObjectProperty

lyrics = ""

class FirstScreen(Screen):
    pass
class SearchLyricsScreen(Screen):
    pass
class StartScreen(Screen):
    pass
class displayLyricsScreen(Screen,BoxLayout):
    getLyrics = StringProperty()
    message = StringProperty()
    btn = ObjectProperty(None)
    def change_text(self):
        self.getLyrics = lyrics
    def removeButton(self):
        self.remove_widget(self.btn)



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

    
    def getLyricsScreen(self):
        self.current = 'SearchLyricsPage'  
    def backToHomeScreen(self):
        self.current = 'start'  
         
    

    




root_widget = Builder.load_string('''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
MyScreenManager:
    transition: FadeTransition()
    FirstScreen:
    StartScreen:
    SearchLyricsScreen:
    displayLyricsScreen:
    
<FirstScreen>:
    name: 'loginPage'
    size_hint: None, None
    size: 300,533
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    elevation: 10
    padding: 25
    spacing: 25
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.size
            
    BoxLayout:
        orientation: 'vertical'
        padding: 25
        spacing: 25
        Label:
            id: welcome_label
            text: "WELCOME"
            font_size:40
            halign: 'center'
            valign: 'top'
            color: 0.3,0.3,0.3,1
            size_hint_y: 1
            height: self.texture_size[1]
            padding_y:30
        
        TextInput:
            id: username
            hint_text: "username"
            font_size: 18
            pos_hint: {"centre_x":0.5}
            size_hint: (1, None)
            height: 35
            multiline: False
            
        
        TextInput:
            id: password
            hint_text: "password"
            font_size: 18
            pos_hint: {"centre_x":0.5}
            size_hint: (1, None)
            height: 35
            multiline: False
            spacing: 10

        Button:
            id: submitLoginButton
            text: "Submit"
            pos_hint: {"centre_x":0.5}
            size_hint: (1, None)
            height: 40
            multiline: False
            on_release: 
                app.root.getLogin()
        
        Button:
            id: registerButton
            text: "Register"
            pos_hint: {"centre_x":0.5}
            size_hint: (1, None)
            height: 40
            multiline: False
            on_release: 
                app.root.getRegistration()
                
<StartScreen>:
    name: 'start'
    size_hint: None, None
    size: 300,533
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    elevation: 10
    padding: 25
    spacing: 25
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.size
    
    Label:
        id: songTitleLable
        text: "Upcoming Karaoke Events"
        font_size:40
        halign: 'center'
        pos_hint: {"x":0,"y":0.8}
        color: 0.3,0.3,0.3,1
        padding_y:30
        text_size: self.width, None
        size_hint: 1, None
            
    BoxLayout:
        orientation: 'vertical'
        padding: 25
        spacing: 25
        

        Button:
            id: submitSongTitle
            text: "Get Lyrics"
            pos_hint: {"centre_x":0.5}
            size_hint: (1, None)
            height: 40
            multiline: False
            on_release: 
                app.root.getLyricsScreen()


<SearchLyricsScreen>:
    name: 'SearchLyricsPage'
    size_hint: None, None
    size: 300,533
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    elevation: 10
    padding: 25
    spacing: 25
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.size
            
    BoxLayout:
        orientation: 'vertical'
        padding: 25
        spacing: 25
        Label:
            id: songTitleLable
            text: "Seach For Song"
            font_size:40
            halign: 'center'
            valign: 'top'
            color: 0.3,0.3,0.3,1
            height: self.texture_size[1]
            padding_y:30
            text_size: self.width, None
            size_hint: 1, None
        
        TextInput:
            id: songTitle
            hint_text: "Title"
            font_size: 18
            pos_hint: {"centre_x":0.5}
            size_hint: (1, None)
            height: 35
            multiline: False
        
        TextInput:
            id: artist
            hint_text: "Artist"
            font_size: 18
            pos_hint: {"centre_x":0.5}
            size_hint: (1, None)
            height: 35
            multiline: False

        Button:
            id: submitSongTitle
            text: "Get Lyrics"
            pos_hint: {"centre_x":0.5}
            size_hint: (1, None)
            height: 40
            multiline: False
            on_release: app.root.getLyrics()
        Button:
            id: backToHome
            text: "Back"
            pos_hint: {"centre_x":0.5}
            size_hint: (1, None)
            height: 40
            multiline: False
            on_release: app.root.backToHomeScreen()

<displayLyricsScreen>:
    btn: remove
    name: 'displayLyricsPage'
    size_hint: None, None
    size: 300,533
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    elevation: 10
    padding: 25
    spacing: 25
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        height: self.minimum_height
        ScrollView:
            do_scroll_x: False
            do_scroll_y: True
            Label:
                text: "start"
                text: root.getLyrics
                font_size:20
                halign: 'center'
                pos_hint: {"x":0,"y":0.8}
                color: 0.3,0.3,0.3,1
                padding_y:30
                text_size: self.width, None
                size_hint: 1, None
        Button:
            text: "start"
            id: remove
            pos_hint: {"centre_x":0.5}
            size_hint: (1, None)
            height: 40
            on_press: 
                root.removeButton()
                root.change_text()
        Button:
            id: backToHome
            text: "Back"
            pos_hint: {"centre_x":0.5}
            size_hint: (1, None)
            height: 40
            multiline: False
            on_release: app.root.backToHomeScreen()
                

''')



class ScreenManagerApp(App):
    def build(self):
        return root_widget

ScreenManagerApp().run()