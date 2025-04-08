from kivy.uix.textinput import TextInput
from functools import partial

class InputManager:

	#n_lines is the number of tries
	def __init__(self, n_lines, n_letters, layout, dictionary, target_word):
		self.lines = [None] * n_lines  # Creates a list with n_lines empty slots
		self.n_lines = n_lines
		self.n_letters = n_letters
		self.layout = layout

		self._create_lines()

		self.start_game()

	def start_game(self):
		self.lines[0].enable_line()  # Enable the first line for input

	#init the lines
	def _create_lines(self):
		for i in range(self.n_lines):  # Loop through all indexes
			self.lines[i] = Line(self.layout, self.n_letters)  # Now it won't go out of range


class Line:

	def __init__(self, layout, n_letters):
		self.layout = layout
		self.current_idx = 0
		self.n_letters = n_letters
		self.inputs = []

		for i in range(n_letters):
			# Create a TextInput widget for each letter, disabled by default
			text_box = TextInput(hint_text=f"Type here {i}", multiline=False, disabled=True, focus=False)
			text_box.bind(text=partial(self._on_text, i))  # Pass the index explicitly

			self.layout.add_widget(text_box)
			self.inputs.append(text_box)  # Assign the TextInput to the list

	# Define the on_text method that will switch focus
	# Callback function: function passed as an argument to another function
	def _on_text(self, idx, instance, value):

		if (len(value) == 1):  # Check if the current text box is filled

			#check if the inserted letter is an alphabetic character
			if (not value.isalpha()):
				instance.text = ""
				return

			# force the letter to be uppercase
			instance.text = instance.text.upper()

			self.current_idx = idx + 1
			if self.current_idx < self.n_letters:  # Ensure we don't go out of bounds
				self.inputs[self.current_idx].focus = True

		# it limits the number of letters to 1 truncate the string when the user types more than 1 letter
		if (len(value) > 1):
			instance.text = value[:1]


	def enable_line(self):

		#enable_line
		for i in range(self.n_letters):
			self.inputs[i].disabled = False

		self.inputs[0].focus = True  # Set focus to the first input