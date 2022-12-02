import more_itertools

from absl import app
from absl import flags
from typing import Sequence


FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')


def read(path: str) -> Sequence[int]:
  with open(path) as f:
    lines = f.read().splitlines()

  is_empty = lambda s: s == ''
  grps = more_itertools.split_at(lines, is_empty)
  return [sum(int(e) for e in grp)
          for grp in grps]


def main(argv):
  calories = read(_INPUT_FILE.value)

  print(f'Max carried: {max(calories)}')
  print(f'Sum of top 3 carried: {sum(sorted(calories)[-3:])}')

if __name__ == '__main__':
  app.run(main)
