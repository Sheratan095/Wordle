from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from InputManager import InputManager
from kivy.uix.boxlayout import BoxLayout



class MyGridLayout(GridLayout):

	def __init__(self, **kwargs):
		super(MyGridLayout, self).__init__(**kwargs)
		self.cols = 5
		self.padding = [10, 10, 10, 10]
		self.spacing = [5, 5]

		self.inputManager = InputManager(6, 5, self)
	
	def start_game(self, target_word):
		self.inputManager.start_game(target_word)
