import kivy
from kivy.app import App #base functionality required to create GUI
from kivy.uix.label import Label #widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from InputManager import InputManager

class MyGridLayout(GridLayout):

	def __init__(self, dictionary, **kwargs):
		super(MyGridLayout, self).__init__(**kwargs)
		self.cols = 5
		self.padding = [10, 10, 10, 10]
		self.spacing = [5, 5]
		# for i in range(6):
		# 	for j in range(5):
		# 		self.text_box  = TextInput(multiline = False)
		# 		self.add_widget(self.text_box)
		self.inputManager = InputManager(6, 5, self, dictionary)
	
	def start_game(self, target_word):
		self.inputManager.start_game(target_word)
		
class WordleApp(App):
	def build(self):
		return MyGridLayout()
	
if __name__ == '__main__':
	WordleApp().run()