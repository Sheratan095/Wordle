import json
from Dictionary import Dictionary


# Open and read the JSON file
# With open ... ensure that the file is automatically closed once the block is exited
#	even if an error occurs
with open("config.json", "r") as file:  # Replace with your JSON file name
	data = json.load(file)

# Retrieve properties
source_file = data["source_file"]
word_len = data["word_length"]
n_tries = data["number_of_tries"]

global_dictionary = Dictionary(word_len)
# load the dictionary
global_dictionary.load_from_file(source_file)
