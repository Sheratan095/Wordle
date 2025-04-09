from kivy.uix.textinput import TextInput
from functools import partial
from kivy.clock import Clock

class Line:

	def __init__(self, layout, n_letters, inputManager):
		self.layout = layout
		self.current_idx = 0
		self.n_letters = n_letters
		self.inputs = []
		self.inputManager = inputManager

		for i in range(n_letters):
			# Create a TextInput widget for each letter, disabled by default
			text_box = TextInput(multiline=False, disabled=True, focus=False, halign="center", font_size="24sp", size_hint = (None, None), width=60, height=60, padding_y = [15, 15])
			text_box.bind(text=partial(self._on_text, i))  # Pass the index explicitly
			text_box.bind(on_text_validate=partial(self._on_enter, i))  # Pass the index explicitly

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

	def _on_enter(self, instance, value):
		self.get_current_word()
	
	def get_current_word(self):
		word = ""
		print("Checking the word")
		for i in range(len(self.inputs)):

			if (len(self.inputs[i].text) == 0):
				print("Empty input at ", i)
				# restote the focus to the first empty input
				# print ("Error, not enough letters")
				self.inputs[i].focus = True
				return
	
			word += self.inputs[i].text
		self.inputManager.check_line(word)  # Call the check_line method in InputManager


	# Called by check_line to color the letters
	#  for each letter in the word, 0 for green, 1 for yellow, 2 for gray
	def color_line(self, check_code):

		if (check_code == "-1"):
			print ("The word is not in the dictionary")
			return

		for i in range(self.n_letters):
			if check_code[i] == '0':
				self.inputs[i].background_color = [0, 1, 0, 1]  # Green
			elif check_code[i] == '1':
				self.inputs[i].background_color = [1, 1, 0, 1]  # Yellow
			elif check_code[i] == '2':
				self.inputs[i].background_color = [0.5, 0.5, 0.5, 1]  # Gray

	def enable_line(self):
		for i in range(self.n_letters):
			self.inputs[i].disabled = False
			self.inputs[i].focus = False

		Clock.schedule_once(self.set_focus, 0.1)

	def set_focus(self, dt):
		self.inputs[0].focus = True
	
	def disable_line(self):
		for i in range(self.n_letters):
			self.inputs[i].disabled = True
			self.inputs[i].focus = False
	
	def clear_line(self):
		for i in range(self.n_letters):
			self.inputs[i].text = ""
			self.inputs[i].background_color = [1, 1, 1, 1]
			self.inputs[i].focus = False  # Explicitly reset focus
			self.disable_line()
