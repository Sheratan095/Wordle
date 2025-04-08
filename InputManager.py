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
