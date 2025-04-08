import random

class Dictionary:

	# the defualt length of the word is 5
	def __init__(self, words_length = 5):
		self.words_length = words_length
		self.words = [] #init an empty list of words
		self.previous_word = "" #init the previous word to None

	# populate the list of words from a specified file
	def load_from_file(self, file_name):

		try:
			file = open(file_name, "r")
		except Exception as ex:
			print("Error: Could not open file")
			return (None)

		for line in file:

			# remove the spaces and new lines from the word
			line = line.strip()

			if (len(line) != self.words_length):
				raise Exception("Error: The word \"{}\" is not of length ({})".format(line, self.words_length))

			self.words.append(line)

		file.close()

	#return a random word from the list of words
	# the word returned should not be the same as the previous one
	def get_random_word(self):

		if (self.previous_word == ""):
			chosen_word = self.generate_random_word()
		else:
			chosen_word = ""
			while ((chosen_word == "") or (chosen_word == self.previous_word)):
				chosen_word = self.generate_random_word()

		self.previous_word = chosen_word

		return (chosen_word)

	def generate_random_word(self):
		index = random.randint(0, len(self.words) - 1)
		return (self.words[index])