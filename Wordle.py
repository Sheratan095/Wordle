from Dictionary import Dictionary

d = Dictionary()

d.load_from_file("test.txt")

print(d.get_random_word())