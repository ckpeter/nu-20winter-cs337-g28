import sys
import os
import json

def write_sample():
  file = sys.argv[1]
  of = os.path.dirname(file) + 'ggsample.json'
  num = 20000
  
  data = None
  
  with open(file) as json_file:
    data = json.load(json_file)
    for v in data:
      # save the original text in a separate field
      v['original'] = v['text']
    
  with open(of, 'w') as outfile:
      json.dump(data[0:num], outfile)
      
  print("Sample written to " + of)
  
if __name__ == "__main__":
  write_sample()