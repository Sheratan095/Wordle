from Line import Line

class InputManager:

	#n_lines is the number of tries
	def __init__(self, n_lines, n_letters, layout, dictionary, target_word):
		self.lines = [None] * n_lines  # Creates a list with n_lines empty slots
		self.n_lines = n_lines
		self.n_letters = n_letters
		self.layout = layout
		self.dictionary = dictionary
		self.target_word = target_word.upper()
		self.current_line = 0
		self._create_lines()

		# to do eliminate
		self.start_game()

	def start_game(self):
		for i in range(self.n_lines):
			self.lines[i].clear_line()
		self.lines[0].enable_line()  # Enable the first line for input

	#init the lines
	def _create_lines(self):
		for i in range(self.n_lines):  # Loop through all indexes
			line = Line(self.layout, self.n_letters, self)
			self.lines[i] = line  # Store the Line instance

	def check_line(self, word):

		# check if the word is in the dictionary
		if (self.dictionary.word_exists(word) == False):
			self.lines[self.current_line].color_line("-1")  # word not valid
			return

		# valid word

		# generate control code
		control_code = self.generate_control_code(word)
		
		self.lines[self.current_line].color_line(control_code)

		#check for the win
		if (control_code.count(control_code[0]) == len(control_code)):
			print("You win")
		else:
			# check if the word is not in the dictionary
			self.lines[self.current_line].disable_line()

			#skip the line
			self.current_line += 1

			# check if the user has used all the tries
			if (self.current_line == self.n_lines):
				print("Game over")
				return

			# go to the next line
			self.lines[self.current_line].enable_line()
	
	def generate_control_code(self, word):

		control_code = ""

		# contains the letters from the target word that aren't in input
		not_found = []

		for i in range(self.n_letters):
			# match = 0 GREEN
			if (self.target_word[i] == word[i]):
				control_code += '0'
			else:
				control_code += '2' # not match = 2 YELLOW
				not_found.append(self.target_word[i])

		for i in range(self.n_letters):

			if (control_code[i] == '2'):

				try:
					index = not_found.index(word[i])
				except ValueError:
					index = -1

				if (index != -1):
					control_code = control_code[:i] + '1' + control_code[i+1:]
					not_found.remove(not_found[index])

		return (control_code)
