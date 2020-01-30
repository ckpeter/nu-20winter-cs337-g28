# nu-20winter-cs337-g28

# setup

Run in python

$ import nltk  
$ nltk.download('punkt')  
$ nltk.download('averaged_perceptron_tagger')  

Also download the given json data files

# Sample

python sample_subset.py gg2013.json

to generate a small data set for faster development runs

# To run

python main.py ggsample.json

which will load data, pre-preprocess, and output some basic guesses.

# Additional work

Implement code to guess host, awards, nominees, presenters, and winners, using the
framework.

Note that most of the tweets are fairly useless, so the approach is to use regex to look for
specific kinds of tweets that would indicate the information, such as
"[someone] won award for [award type]"

The basic framework is that the the data is loaded, then some preprocessing is done,
mostly in tokenizing and in removing duplicate tweets. Then each tweet is fed to a
function that will evaluate it and extract useful information. The extracted information is
then stored in the "ideas" variable, which is basically a dictionary that holds various kinds
of guesses and votes.

As additional rules are adding for extraction, the single function will probably become
many functions, each specializing in extracting a particular kind of information, such as
presenters or award names.

Once all the tweets are processed, the ideas variable should hold all relevant information,
and a final output processing code can be used to select information based on votes,
associate like terms, and eventually output the required answers.

