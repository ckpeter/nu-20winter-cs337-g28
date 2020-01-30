# nu-20winter-cs337-g28

# setup

Run in python

$ import nltk  
$ nltk.download('punkt')  
$ nltk.download('averaged_perceptron_tagger')  

Also download the given json data files

# Sample

python sample_subset.py gg2013.json

to generate a small data set for testing

# To run

python main.py ggsample.json

which will load data, pre-preprocess, and output some basic guesses.

# Additional work

Implement code to guess host, awards, nominees, presenters, and winners, using the
framework.

Note that most of the tweets are fairly useless, so the approach is to use regex to look for
specific kinds of tweets that would indicate the information, such as
"[someone] won award for [award type]"

