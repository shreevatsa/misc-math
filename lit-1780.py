def split_by(stream, pattern):
  for multi_sentence in stream:
    for sentence in multi_sentence.split(pattern):
      if sentence:
        yield sentence

def all_sentences(text):
  """Finds "sentences" in a "text"."""
  sentencesA = text.split('\r\n\r\n')
  sentences0 = split_by(sentencesA, '.\r\n')
  sentences1 = split_by(sentences0, '.  ')
  sentences2 = split_by(sentences1, '!  ')
  sentences3 = split_by(sentences2, '?  ')
  sentences4 = split_by(sentences3, '. ')  # with heavy heart...
  return sentences4

def all_words(sentence):
    """Finds "words" in a "sentence"."""
    words0 = sentence.split(' ')
    words1 = split_by(words0, '\r\n')
    words2 = split_by(words1, '--')
    return words2

print 'Opening the file and reading.'
text = open('/Users/srajagopalan/Downloads/pg3200.txt').read()
print 'Done reading, got text of length', len(text), '-- now getting sentences'
sentences = list(all_sentences(text))
print 'Got', len(sentences), 'sentences, now getting words for each'
length_sentences = [(len(list(all_words(sentence))), sentence) for sentence in sentences]
print 'Split them into words; now sorting and reversing'
length_sentences.sort()
length_sentences.reverse()
for length, sentence in length_sentences[:1]:
  print (length, sentence)
  print length
  print sentence
  print
  print
