import kivy
from kivy.app import App #base functionality required to create GUI
from kivy.uix.label import Label #widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from InputManager import InputManager
from Dictionary import Dictionary

dictionary = Dictionary()
dictionary.load_from_file("test.txt")

# target_word = dictionary.get_random_word()

# target_word = "ARISE"
#try with ariot

target_word = "MIROC"

class MyGridLayout(GridLayout):

	def __init__(self, **kwargs):
		super(MyGridLayout, self).__init__(**kwargs)
		self.cols = 5

		# for i in range(6):
		# 	for j in range(5):
		# 		self.text_box  = TextInput(multiline = False)
		# 		self.add_widget(self.text_box)
		InputManager(6, 5, self, dictionary, target_word)
		
class WordleApp(App):
	def build(self):
		return MyGridLayout()
	
if __name__ == '__main__':
	WordleApp().run()