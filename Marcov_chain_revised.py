
# Use pride and prejudice
!curl https://www.gutenberg.org/files/1342/1342-0.txt | tail -n+32 > /content/pride-and-prejudice.txt
!head -n 10 /content/pride-and-prejudice.txt

import numpy as np
import random
import re
from collections import defaultdict

path = '/content/pride-and-prejudice.txt'
with open(path) as f:
  text = f.read()
tokenized_text = [
    word
    for word in re.split('\W+', text)
    if word != ''
]

# Create graph.
markov_graph = defaultdict(lambda: defaultdict(int))



#last_word = tokenized_text[0].lower()
#for word in tokenized_text[1:]:
#  word = word.lower()
#  markov_graph[last_word][word] += 1
#  last_word = word

last_word = tokenized_text[0].lower()
for word in tokenized_text[1:]:
  word = word.lower()
  markov_graph[last_word][word] += 1
  last_word = word

# Preview graph.
limit = 3
for first_word in ('the', 'by', 'who'):
  next_words = list(markov_graph[first_word].keys())[:limit]
  for next_word in next_words:
    print(first_word, next_word)

    def walk_graph(graph, distance=5, start_node=None):
      """Returns a list of words from a randomly weighted walk."""
      if distance <= 0:
        return []

      # If not given, pick a start node at random.
      if not start_node:
        start_node = random.choice(list(graph.keys()))


      weights = np.array(
          list(markov_graph[start_node].values()),
          dtype=np.float64)
      # Normalize word counts to sum to 1.
      weights /= weights.sum()

      # Pick a destination using weighted distribution.
      choices = list(markov_graph[start_node].keys())
      chosen_word = np.random.choice(choices, None, p=weights)

      return [chosen_word] + walk_graph(
          graph, distance=distance-1,
          start_node=chosen_word)

    for i in range(10):
      print(' '.join(walk_graph(
          markov_graph, distance=12)), '\n')
