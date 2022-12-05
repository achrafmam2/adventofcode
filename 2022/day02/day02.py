from absl import app
from absl import flags
from typing import Sequence

import enum
import functools


FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')


@functools.total_ordering
class Shape(enum.Enum):
  ROCK = 1
  PAPER = 2
  SCISSOR = 3

  @property
  def score(self):
    return self.value

  def __ge__(self, other):
    if (self == Shape.ROCK and other == Shape.SCISSOR) or (
        self == Shape.PAPER and other == Shape.ROCK) or (
          self == Shape.SCISSOR and other == Shape.PAPER):
      return True
    return False

  def cmp(self, other):
    if self == other:
      return 0
    if self > other:
      return 1
    return -1


def parse(path: str) -> Sequence[tuple[str, str]]:
  with open(path) as f:
    return [tuple(l.split(' ')) for l in f.read().splitlines()]


def compute_score(rounds: Sequence[tuple[Shape, Shape]]) -> int:
  score = 0
  for (other, me) in rounds:
    score += me.score
    if me > other:
      score += 6
    elif me == other:
      score += 3

  return score
  
def part1(rounds: Sequence[tuple[str, str]]):
  shape = {
    'A': Shape.ROCK, 'B': Shape.PAPER, 'C': Shape.SCISSOR,
    'X': Shape.ROCK, 'Y': Shape.PAPER, 'Z': Shape.SCISSOR,    
  }

  rounds = [(shape[a], shape[b]) for (a, b) in rounds]
  print('total score: ', compute_score(rounds))


def part2(rounds: Sequence[tuple[str, str]]):
  shape = {
    'A': Shape.ROCK, 'B': Shape.PAPER, 'C': Shape.SCISSOR,
  }

  outcome = {
    'X': -1, # Lose.
    'Y': 0,  # Draw.
    'Z': 1,  # Win.
  }

  rs = []
  for (a, b) in rounds:
    other, want_outcome = shape[a], outcome[b]

    found = False
    for me in [Shape.ROCK, Shape.PAPER, Shape.SCISSOR]:
      if me.cmp(other) == want_outcome:
        rs.append((other, me))
        found = True
        break

    assert found

  print('total score: ', compute_score(rs))        

def main(argv):
  rounds = parse(_INPUT_FILE.value)
  part1(rounds)
  part2(rounds)
  

if __name__ == '__main__':
  app.run(main)
