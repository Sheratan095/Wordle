from kivy.app import App
from Line import Line
from kivy.clock import Clock
from kivy.core.window import Window
from Globals import *


class InputManager:

	#n_lines is the number of tries
	def __init__(self, layout):
		self.n_lines = n_tries
		self.lines = [None] * self.n_lines  # Creates a list with n_lines empty slots
		self.layout = layout
		self.current_line = 0
		self._create_lines()

	def start_game(self, target_word):

		# Hide the cursor
		Window.show_cursor = False

		self.target_word = target_word.upper()
		for i in range(self.n_lines):
			self.lines[i].clear_line()  # Clear all lines and reset focus
		self.current_line = 0

		Clock.schedule_once(lambda dt: self.lines[0].enable_line(), 0.1)  # Enable the first line with a slight delay

	#init the lines
	def _create_lines(self):
		for i in range(self.n_lines):  # Loop through all indexes
			line = Line(self.layout, word_len, self)
			self.lines[i] = line  # Store the Line instance

	def check_line(self, word):

		# check if the word is in the dictionary
		if (global_dictionary.word_exists(word) == False):
			self.lines[self.current_line].color_line("-1")  # word not valid
			return

		# word is valid

		# generate control code
		control_code = self._generate_control_code(word)
		
		self.lines[self.current_line].color_line(control_code)

		#check for the win
		if (control_code.count(control_code[0]) == len(control_code)):
			Window.show_cursor = True

			print("You win")
			App.get_running_app().root.current = 'victory'
		else:

			self.lines[self.current_line].disable_line()

			#skip the line
			self.current_line += 1

			# check if the user has used all the tries
			if (self.current_line == self.n_lines):

				Window.show_cursor = True

				print("Game over")
				App.get_running_app().root.current = 'defeat'

				return

			# go to the next line
			self.lines[self.current_line].enable_line()
	
	def _generate_control_code(self, word):

		control_code = ""

		# contains the letters from the target word that aren't in input
		not_found = []

		for i in range(word_len):
			# match = 0 GREEN
			if (self.target_word[i] == word[i]):
				control_code += '0'
			else:
				control_code += '2' # not match = 2 YELLOW
				not_found.append(self.target_word[i])

		for i in range(word_len):

			if (control_code[i] == '2'):

				try:
					index = not_found.index(word[i])
				except ValueError:
					index = -1

				if (index != -1):
					control_code = control_code[:i] + '1' + control_code[i+1:]
					not_found.remove(not_found[index])

		return (control_code)
