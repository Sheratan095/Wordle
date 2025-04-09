from kivy.uix.textinput import TextInput
from functools import partial
from kivy.clock import Clock
from kivy.uix.popup import Popup
from  kivy.uix.label import Label

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

			 # Use a wrapper function to handle key_down events
			def key_down_wrapper(window, keycode, text, modifiers, idx=i):
				return self._keyboard_on_key_down(idx, text_box, window, keycode, text, modifiers)

			text_box.keyboard_on_key_down = key_down_wrapper  # Assign the wrapper function

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
		if (len(value) > 2):
			instance.text = value[:1]
		
		if (len(value) == 2):
			instance.text = value[1]

	# Compose the word from the letters in the line
	def get_current_word(self):
		word = ""
		for i in range(len(self.inputs)):
			if (len(self.inputs[i].text) == 0):
				self.inputs[i].focus = True
				return (None)

			word += self.inputs[i].text

		return (word.upper())

	# Called by check_line to color the letters
	#  for each letter in the word, 0 for green, 1 for yellow, 2 for gray
	def color_line(self, check_code):

		if (check_code == "-1"):
			popup = Popup(title='Warning', content=Label(text='Invalid word!'), size_hint=(.5, .5))
			print ("The word is not in the dictionary")
			popup.open()
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

	#Clock.schedule_once(self.set_focus, 0.1) because Kivy's UI updates happen asynchronously.
	# if self.inputs[0].focus = True is setted immediately after enabling the inputs, Kivy might not yet have completed updating the UI.
	#By scheduling self.set_focus to run after a short delay (0.1 seconds):
	#The UI has fully processed enabling the inputs.
	#The first input field can properly receive focus.

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


	def _keyboard_on_key_down(self, idx, instance, window, keycode, text, modifiers):

		if (keycode[1] == 'backspace'):  # Check if the key pressed is backspace

			self.current_idx = idx

			if (len(self.inputs[idx].text) > 0):  # If the current box is not empty, clear it
				self.inputs[idx].text = ""
			elif (idx > 0):  # If the current box is empty and not the first box, move focus back
				self.inputs[idx].focus = False  # Remove focus from the current box
				self.current_idx = self.current_idx - 1
				self.inputs[self.current_idx].focus = True  # Set focus to the previous box
				self.inputs[self.current_idx].text = ""  # Clear the previous box

			return (True)  # Intercept the backspace action even if no action is needed

		if (keycode[1] == 'enter'):  # Check if the key pressed is enter

			word = self.get_current_word()

			if (word == None):
				popup = Popup(title='Warning', content=Label(text='Input five letters!'), size_hint=(.5, .5))
				popup.open()
			else:
				self.inputManager.check_line(word)  # Call the check_line method in InputManager

			return (True)  # Intercept the enter action

		if (keycode[1] == 'left'):  # Check if the key pressed is left arrow

			if (idx > 0):
				self.inputs[self.current_idx - 1 ].focus = False
				self.current_idx = idx - 1
				self.inputs[self.current_idx].focus = True

			return (True)  # Intercept the left arrow action

		if (keycode[1] == 'right'):  # Check if the key pressed is right arrow

			if (idx < self.n_letters - 1):
				self.inputs[self.current_idx].focus = False
				self.current_idx = idx + 1
				self.inputs[self.current_idx].focus = True
	
			return (True)  # Intercept the right arrow action

		return (False)  # Allow other keys to behave normally
