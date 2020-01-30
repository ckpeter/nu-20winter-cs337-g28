import json
import nltk
import re
import sys

## gg2013/5/2020.json
file = sys.argv[1]

# These are definitely not hosts, awards, and not winners
# e.g. 'just won', 'she wins'
stops = ['just', 'he', 'she', 'have', 'you', "n't", 'patriots', 'pats',
'should', 'will/should', 'already', 'a', 'an', 'the', 'will', 'would']
min_len = 3

def main():
  data = read_file(file)
  print("%%%%%%%%% BEGIN RUN " + str(len(data)) + " %%%%%%%%% " + file)
  
  if False:
    print_tw(data)
    
  data = preprocess_data(data)
  print("%%%%%%%%% Pre-precessing completed %%%%%%%%% ")
  out = {}
  ideas = {
    'winners': {}, # List of candidate winner names
    'awards': {}, # List of candidate award names
    'links': {}, # List of candidate winner=award pairing
    'xx': {}
  }
  
  for tw in data:
    eval_tw(tw, ideas)
  
  print_votes(ideas['awards'])

"""
Given one tweet, evaluate it, and if it fits the target goal, add to the votes.
"""
def eval_tw(tw, ideas):
  winners = ideas['winners']
  awards = ideas['awards']
  links = ideas['links']
  
  for k, tk in enumerate(tw['tokens']):
    #if k > 0 and re.match(r'^(win|wins|won)$', tk):
    if k > 0 and re.match(r'^(nominated)$', tk):
      # TODO smarter way of finding the subject than just going back by 1?
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

def print_votes(votes, detailed=True):
  keys = sorted(votes.keys(), reverse=False, key=lambda x: len(votes[x]))
  
  if detailed:
    lines = map(
      lambda k: "===== " + k + " (" + str(len(votes[k])) + " votes) =====\n" +
      "\n".join(map(lambda xx: str(xx), votes[k])), keys)
  else:
    lines = map(
      lambda k: "===== " + k + " (" + str(len(votes[k])) + " votes) =====\n", keys)
    
  print("\n".join(lines))

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
  
def print_tw(tws):
  if False:
    print("\n\n=== ".join([str(nltk.word_tokenize(x['text'])) for x in tws]))
  else:
    print("\n\n=== ".join([x['text'] for x in tws]))

def nldk_demo():
	sentence = """At eight o'clock on Thursday morning
... Arthur didn't feel very good."""
	tokens = nltk.word_tokenize(sentence)
	tagged = nltk.pos_tag(tokens)
	tagged[0:6]
	print(tokens)

if __name__ == "__main__":
  main() if True else nldk_demo()
