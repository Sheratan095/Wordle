from Dictionary import Dictionary

d = Dictionary(5)

d.load_from_file("words.txt")


print(d.get_random_word())
print(d.get_random_word())
print(d.get_random_word())
print(d.get_random_word())

