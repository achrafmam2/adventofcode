from absl import app
from absl import flags
from typing import Sequence


FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')


def priority(c: str) -> int:
  assert(len(c) == 1)    
  if c.islower():
    return ord(c) - ord('a') + 1
  return ord(c) - ord('A') + 27


def parse(path: str) -> Sequence[str]:
  with open(path, 'r') as f:
    return f.read().splitlines()

def part1(rucksacks: Sequence[str]):
  score = 0
  for r in rucksacks:
    n = len(r) // 2
    l, r = set(r[:n]), set(r[n:])
    
    [c] = l.intersection(r)
    score += priority(c)
    
  print(score)


def part2(rucksacks: Sequence[str]):
  # See https://stackoverflow.com/a/1625023
  triplets = zip(*((iter(rucksacks),) * 3))

  score = 0
  for (r0, r1, r2) in triplets:
    r0, r1, r2 = set(r0), set(r1), set(r2)
    [c] = r0.intersection(r1).intersection(r2)
    score += priority(c)
  print(score)


def main(argv):
  rucksacks = parse(_INPUT_FILE.value)
  part1(rucksacks)
  part2(rucksacks)

if __name__ == '__main__':
  app.run(main)
