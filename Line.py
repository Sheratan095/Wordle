from kivy.uix.textinput import TextInput
from functools import partial
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

class Line:

	def __init__(self, layout, n_letters, inputManager):
		self.layout = layout
		self.current_idx = 0
		self.n_letters = n_letters
		self.inputs = []
		self.inputManager = inputManager
		self.popupOpen = False

		for i in range(n_letters):
			# Create a TextInput widget for each letter, disabled by default
			text_box = TextInput(multiline=False, disabled=True, focus=False, halign="center", font_size="24sp", size_hint = (None, None), width=60, height=60, padding_y = [15, 15])
			
			# Disable mouse clicks on the TextInput
			def disable_mouse_click(instance, touch):
				return (True)  # Intercept and stop the touch event

			text_box.on_touch_down = lambda touch, instance=text_box: disable_mouse_click(instance, touch)  # Properly pass the `touch` argument

			# Use a wrapper function to handle key_down events
			def key_down_wrapper(window, keycode, text, modifiers, idx=i):
				return (self._keyboard_on_key_down(idx, text_box, window, keycode, text, modifiers))

			text_box.keyboard_on_key_down = key_down_wrapper  # Assign the wrapper function

			text_box.bind(text=partial(self._on_text, i))  # Pass the index explicitly

			self.layout.add_widget(text_box)
			self.inputs.append(text_box)  # Assign the TextInput to the list


	# Define the on_text method that will switch focus
	# Callback function: function passed as an argument to another function
	def _on_text(self, idx, instance, value):

		if (self.popupOpen):
			instance.text = ""
			return

		if (len(value) == 1):  # Check if the current text box is filled

			#check if the inserted letter is an alphabetic character
			if (not value.isalpha()):
				instance.text = ""
				return

			# force the letter to be uppercase
			instance.text = instance.text.upper()

			self.current_idx = idx + 1
			if (self.current_idx < self.n_letters):  # Ensure we don't go out of bounds
				self.inputs[self.current_idx].focus = True
			else:
				self.current_idx = self.current_idx - 1

		# it limits the number of letters to 1 truncate the string when the user types more than 1 letter
		if (len(value) > 1):
			instance.text = value[:1]

	# Compose the word from the letters in the line
	def _get_current_word(self):
		word = ""
		for i in range(len(self.inputs)):

			if (len(self.inputs[i].text) == 0):
				# restote the focus to the first empty input
				self.inputs[i].focus = True
				return (None)

			word += self.inputs[i].text

		return (word.upper())

	# Called by check_line to color the letters
	#  for each letter in the word, 0 for green, 1 for yellow, 2 for gray
	def color_line(self, control_code):

		if (control_code == "-1"):
			self._create_popup("Word not in dictionary")
			return

		for i in range(self.n_letters):
			if control_code[i] == '0':
				self.inputs[i].background_color = [0, 1, 0, 1]  # Green
			elif control_code[i] == '1':
				self.inputs[i].background_color = [1, 1, 0, 1]  # Yellow
			elif control_code[i] == '2':
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

		if (keycode[1] == 'backspace' and self.popupOpen == False):  # Check if the key pressed is backspace

			if (len(self.inputs[self.current_idx].text) == 0):  # If the current box is empty, move focus back

				if (self.current_idx > 0):
					self.current_idx = idx - 1
					self.inputs[self.current_idx].focus = True
					self.inputs[self.current_idx].text = ""  # Clear the previous box
			else:
				self.inputs[self.current_idx].text = ""

			return (True)  # Intercept the backspace action


		if (keycode[1] == 'enter'):  # Check if the key pressed is enter

			if (self.popupOpen == True):
				self.popup.dismiss(force=True)
				return (True)

			word = self._get_current_word()

			if (word == None):
				self._create_popup("Too short")
			else:
				self.inputManager.check_line(word)  # Call the check_line method in InputManager

			return (True)  # Intercept the enter action

		if (keycode[1] == 'left' and self.popupOpen == False):  # Check if the key pressed is left arrow

			if (idx > 0):
				self.inputs[self.current_idx - 1 ].focus = False
				self.current_idx = idx - 1
				self.inputs[self.current_idx].focus = True

			return (True)  # Intercept the left arrow action

		if (keycode[1] == 'right' and self.popupOpen == False):  # Check if the key pressed is right arrow

			if (idx < self.n_letters - 1):
				self.inputs[self.current_idx].focus = False
				self.current_idx = idx + 1
				self.inputs[self.current_idx].focus = True
	
			return (True)  # Intercept the right arrow action

		# intercept the escape key when the popup is open and close it
		if (keycode[1] == 'escape'):
			if (self.popupOpen == True):
				self.popup.dismiss(force=True)
				return (True)

		return (False)  # Allow other keys to behave normally

	def _create_popup(self, message):

		Window.show_cursor = True

		self.popupOpen = True
		layout = BoxLayout(orientation = 'vertical', spacing = 10, padding = 10)
		label = Label(text=message)
		button = Button(text="Resume")
		layout.add_widget(label)
		layout.add_widget(button)
		self.popup = Popup(title='Warning', content = layout, size_hint=(.5, .5), auto_dismiss=False)
		button.bind(on_release=lambda instance: self.popup.dismiss())
		self.popup.bind(on_dismiss=self.on_popup_dismiss)
		self.popup.open()

	def on_popup_dismiss(self, instance):
		self.popupOpen = False
		self.inputs[self.current_idx].focus = True
		Window.show_cursor = False
		