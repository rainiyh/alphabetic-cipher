import random

# Loads the words into a list to be checked against
def load_words():
	with open('words.txt', 'r') as f:
		word_list = [line.strip() for line in f.readlines()]
	return word_list
	
# Do decoding here
def decode():
	pass

# Do the decoding here
def main():
	load_words()

if (__name__ == "__main__"):
	main()
