import string

def preProcess(word):
  word = word.strip(string.punctuation).lower()
  return word
