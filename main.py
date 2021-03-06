import json
from nltk import word_tokenize, pos_tag
import re
import sys

import process_data

import random

## gg2013/5/2020.json
file = sys.argv[1]

# These are definitely not hosts, awards, and not winners
# e.g. 'just won', 'she wins'
stops = ['just', 'he', 'she', 'have', 'you', "n't", 'patriots', 'pats',
'should', 'will/should', 'already', 'a', 'an', 'the', 'will', 'would', 'for', 'at', 'in', '!', '#']
back_stops = ['\B\@\w+', '']
min_len = 3

def main():
  data = process_data.read_file(file)
  print("%%%%%%%%% BEGIN RUN " + str(len(data)) + " %%%%%%%%% " + file)
  
  if False:
    print_tw(data)
    
  data = process_data.preprocess_data(data)
  print("%%%%%%%%% Pre-precessing completed %%%%%%%%% ")
  out = {}
  ideas = {
    'winners': {}, # List of candidate winner names
    'awards': {}, # List of candidate award names
    'links': {}, # List of candidate winner=award pairing
    'xx': {}
  }
  
  award_names = [
    'best motion picture',
    'best director',
    'best actor',
    'best actress',
    'best supporting actor',
    'best supporting actress',
    'best screenplay',
    'best original score',
    'best original song',
    'cecil b demille'
  ]

  for award_name in award_names:
    ideas['winners'][award_name] = {}

  for tw in data:
    # eval_tw(tw, ideas)
    guess_award_names(tw, ideas)
    ideas['winners'] = guess_winners(tw, ideas, award_names)
  
  answers = {}
  answers['awards'] = []
  answers['winners'] = []

  award_candidates = print_votes(ideas['awards'], detailed=False)
  for i in range(1, 11):
    answers['awards'].append(award_candidates[-i])

  for award in award_names:
    candidates = print_votes(ideas['winners'][award], detailed=False)
    if len(candidates) < 1:
      answers['winners'].append("None Found")
    else:
      answers['winners'].append(candidates[-1])

  output_readable(answers, award_names)


"""
Given one tweet, evaluate it, and if it fits the target goal, add to the votes.
"""
def eval_tw(tw, ideas):
  winners = ideas['winners']
  awards = ideas['awards']
  links = ideas['links']
  
  for k, tk in enumerate(tw['tokens']):
    #if k > 0 and re.match(r'^(nominated)$', tk): # For nominees and awards
    if k > 0 and re.match(r'^(win|wins|won)$', tk):
      subj = tw['tokens'][k-1].lower()
      aw = " ".join(tw['tokens'][k+1:k+4]).lower()
      link = subj + "=" + aw
      
      if subj in stops or len(subj) < min_len:
        continue
      
      if not subj in winners:
        winners[subj] = []
      
      if not aw in awards:
        awards[aw] = []
      
      if not link in links:
        links[link] = []
            
      # Note that when voting, we are not just adding 1, we add a full array
      # [vote, text]
      # This helps in debugging to see what tweets are leading to the votes
      winners[subj].append([1, tw['text']])
      awards[aw].append([1, tw['text']])
      links[link].append([1, tw['text']])

def guess_award_names(tw, ideas):
  awards = ideas['awards']

  # Hypothesis: award names are preceded by "wins best"
  hypothesis = "wins best"
  max_len = 6

  # Search for occurance of hypothesis
  if re.search(hypothesis, tw['text'].lower()):

    # Isolate text after hypothesis keywords, cut down to 4 words max or until stop
    rest_of_tweet = "best" + re.split(hypothesis, tw['text'].lower())[1]
    rest_of_tweet_tokens = word_tokenize(rest_of_tweet)
    
    for i, token in enumerate(rest_of_tweet_tokens):
      if token in stops:
        rest_of_tweet_tokens = rest_of_tweet_tokens[:i]
    if len(rest_of_tweet_tokens) > max_len:
      rest_of_tweet_tokens = rest_of_tweet_tokens[:max_len]

    award_name = " ".join(rest_of_tweet_tokens)

    # Awards: Key: name of award Value: list of all tweets referenceing award name
    if not award_name in ideas['awards']:
      awards[award_name] = []

    awards[award_name].append([1, tw['text']])

def guess_winners(tw, ideas, award_names):
  winners = ideas['winners']

  # See if the tweet contains "...wins [some name of award]"
  for award_name in award_names:
    hypothesis = "wins " + award_name

    if re.search(hypothesis, tw['text'].lower()):
      tweet_beginning = re.split(hypothesis, tw['text'])[0]
      tweet_beginning_tokens = word_tokenize(tweet_beginning)

      # Iterate through tokens backwards to find potential stops
      # for range(len(tweet_beginning_tokens), 0, -1):
      
      if not tweet_beginning in winners[award_name]:
        winners[award_name][tweet_beginning] = []
      

      winners[award_name][tweet_beginning].append([1, tw['text']])

  return winners


def print_votes(votes, detailed=True):
  keys = sorted(votes.keys(), reverse=False, key=lambda x: len(votes[x]))
  
  if detailed:
    lines = map(
      lambda k: "===== " + k + " (" + str(len(votes[k])) + " votes) =====\n" +
      "\n".join(map(lambda xx: str(xx), votes[k])), keys)
  else:
    lines = map(
      lambda k: "===== " + k + " (" + str(len(votes[k])) + " votes) =====\n", keys)
    
  # print("\n".join(lines))
  return keys

def output_readable(answers, awards):
  print("Host: None\n")
  for i, award in enumerate(awards):
    print("True Award Name: " + award)
    print("Closest guessed award name: " + answers['awards'][i])
    print("Presenter: ")
    print("Nominees: ")
    print("Winner: " + answers['winners'][i])


def format_output(ideas, award_names):
  output = {}
  output['host'] = ""
  output['award_data'] = {}
  for award in award_names:
    output['award_data'][award] = {}
    output['award_data'][award]['nominees'] = []
    output['award_data'][award]['presenters'] = []
    output['award_data'][award]['winner'] = ""


  for award in award_names:
    pass

  return output

def goal_list(data, out):
  """
  ## Basic goals:
  ## Host(s) (for the entire ceremony)
  ## Award Names
  ## Presenters, mapped to awards*
  ## Nominees, mapped to awards*
  ## Winners, mapped to awards*
  """
  """
  Red carpet – For example, determine who was best dressed, worst dressed, most discussed, most controversial, or perhaps find pictures of the best and worst dressed, etc.
  Humor – For example, what were the best jokes of the night, and who said them?
  Parties – For example, what parties were people talking about the most? Were people saying good things, or bad things?
  Sentiment – What were the most common sentiments used with respect to the winners, hosts, presenters, acts, and/or nominees?
  Acts – What were the acts, when did they happen, and/or what did people have to say about them?
  Your choice – If you have a cool idea, suggest it to the TA! Ideas that will require the application of NLP and semantic information are more likely to be approved.
  """
  pass
  
  
def print_tw(tws):
  if False:
    print("\n\n=== ".join([str(word_tokenize(x['text'])) for x in tws]))
  else:
    print("\n\n=== ".join([x['text'] for x in tws]))

def nldk_demo():
	sentence = """At eight o'clock on Thursday morning
... Arthur didn't feel very good."""
	tokens = word_tokenize(sentence)
	tagged = pos_tag(tokens)
	tagged[0:6]
	print(tokens)

if __name__ == "__main__":
  main() if True else nldk_demo()
