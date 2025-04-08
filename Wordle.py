from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
import random

class Wordle(App):

	def build(self):
		layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

		# Create two TextInput widgets
		self.textinput1 = TextInput(hint_text="Type here (1)", multiline=False)
		self.textinput2 = TextInput(hint_text="Type here (2)", multiline=False)

		# Bind the on_text event to switch focus between the inputs
		self.textinput1.bind(text=self.on_text)
		self.textinput2.bind(text=self.on_text)

		# Add both TextInput widgets to the layout
		layout.add_widget(self.textinput1)
		layout.add_widget(self.textinput2)

		return layout

	# Define the on_text method that will switch focus
	def on_text(self, instance, value):
		print("on_text")
		# Switch focus when a letter is typed (i.e., when the length of the text changes)
		if len(value) > 0:  # A character was typed
			# Check which TextInput triggered the event and switch focus
			if instance == self.textinput1:
				self.textinput2.focus = True  # Set focus on the second TextInput
			else:
				self.textinput1.focus = True  # Set focus on the first TextInput

if __name__ == "__main__":
	Wordle().run()
