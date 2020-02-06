import json
import nltk

def read_file(file):
  with open(file) as json_file:
    data = json.load(json_file)
    for v in data:
      # save the original text in a separate field
      v['original'] = v['text']
    return data

def preprocess_data(data):
  # Remove dups
  data = sorted(data, key=lambda x: x['text'])
  last = None
  new_data = []
  
  for tw in data:
    if last != tw['text']:
      new_data.append(tw)
      last = tw['text']
    
  data = new_data
  
  # Tokenize
  for tw in data:
    tw['tokens'] = nltk.word_tokenize(tw['text'])

  return data