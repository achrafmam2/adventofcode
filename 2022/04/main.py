from absl import app
from absl import flags
from typing import Sequence

FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')

Range = tuple[int, int]


def parse(path: str) -> Sequence[tuple[Range, Range]]:

  def parse_range(r: str) -> Range:
    [a, b] = r.split('-')
    return (int(a), int(b))

  def parse_line(line: str) -> tuple[Range, Range]:
    [a, b] = line.split(',')
    return (parse_range(a), parse_range(b))

  with open(path, 'r') as f:
    return [parse_line(l) for l in f.read().splitlines()]


def contained(r: Range, s: Range) -> bool:
  a, b = r
  x, y = s
  return a <= x and y <= b


def full_overlap(r: Range, s: Range) -> bool:
  return contained(r, s) or contained(s, r)


def overlap(r: Range, s: Range) -> bool:
  a, b = r
  x, y = s
  return (x <= b) and (a <= y)


def main(argv):
  ranges = parse(_INPUT_FILE.value)

  print(sum(1 for (r0, r1) in ranges if full_overlap(r0, r1)),
        sum(1 for (r0, r1) in ranges if overlap(r0, r1)))


if __name__ == '__main__':
  app.run(main)
