import json
from Dictionary import Dictionary
from TextInputParameters import TextInputParameters


# Open and read the JSON file
# With open ... ensure that the file is automatically closed once the block is exited
#	even if an error occurs
with open("config.json", "r") as file:  # Replace with your JSON file name
	data = json.load(file)

icon = data["icon"]

# Retrieve properties
source_file = data["source_file"]
word_len = data["word_length"]
n_tries = data["number_of_tries"]

credits = data["credits"]
credits_font_size = data["credits_font_size"]
credits_color = data["credits_color"]


# Retrieve parameters for the text input
params = data["text_input_paramters"]
text_input_params = TextInputParameters(
	width=params["width"],
	height=params["height"],
	font_size=params["font_size"],
	padding_y=params["padding_y"]
)

global_dictionary = Dictionary(word_len)
# load the dictionary
global_dictionary.load_from_file(source_file)
