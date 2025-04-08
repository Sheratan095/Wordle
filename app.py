import kivy
from kivy.app import App #base functionality required to create GUI
from kivy.uix.label import Label #widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class MyGridLayout(GridLayout):
	def __init__(self, **kwargs):
		super(MyGridLayout, self).__init__(**kwargs)
		self.cols = 5

		for i in range(30):
			self.text_box  = TextInput(multiline = False)
			self.add_widget(self.text_box)
		

class WordleApp(App):
	def build(self):
		return MyGridLayout()
	
if __name__ == '__main__':
	WordleApp().run()