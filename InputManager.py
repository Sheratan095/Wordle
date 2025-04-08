from Line import Line

class InputManager:

	#n_lines is the number of tries
	def __init__(self, n_lines, n_letters, layout, dictionary, target_word):
		self.lines = [None] * n_lines  # Creates a list with n_lines empty slots
		self.n_lines = n_lines
		self.n_letters = n_letters
		self.layout = layout
		self.dictionary = dictionary
		self.target_word = target_word
		self.current_line = 0

		self._create_lines()

		self.start_game()

	def start_game(self):
		self.lines[0].enable_line()  # Enable the first line for input

	#init the lines
	def _create_lines(self):
		for i in range(self.n_lines):  # Loop through all indexes
			line = Line(self.layout, self.n_letters, self)
			self.lines[i] = line  # Store the Line instance

	def check_line(self, word):

		print("target", self.target_word)
		print("word", word)

		# check if the word is in the dictionary
		if (self.dictionary.word_exists(word) == False):
			self.lines[self.current_line].color_line("-1")  # Color the line red
			return

		win = True
		check_code = ""
		for i in range(self.n_letters):
			# match = 0
			if (word[i] == self.target_word[i]):
				check_code += '0'
			#exist = 1
			elif (word[i] in self.target_word):
				win = False
				check_code += '1'
			#not exist = 2
			else:
				win = False
				check_code += '2'
		print("check_code", check_code)
		self.lines[self.current_line].color_line(check_code)

		if (win == True):
			print("You win")