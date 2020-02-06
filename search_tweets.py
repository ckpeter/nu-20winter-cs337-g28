import json
import nltk
import re
import sys

import process_data

file = sys.argv[1]
data = process_data.read_file(file)

data = process_data.preprocess_data(data)
print("%%%%%%%%% Pre-precessing completed %%%%%%%%% ")

while True:
    query = input("Search tweets using RegEx. To quit, enter 'quit'.>>")
    if query == "quit":
        break

    else:
        for tw in data:
            for tk in tw['tokens']:
                if re.match(query, tk):
                    print(tw['text'])
