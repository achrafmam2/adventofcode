from absl import app
from absl import flags
from typing import Any

import copy

FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')


def parse(path: str) -> list[int]:
  with open(path) as f:
    return [int(l) for l in f.read().splitlines()]


def mixin(xs: list[int], repeat=1) -> list[int]:
  n = len(xs)
  xs = copy.copy(xs)
  idxs = list(range(n))

  for _ in range(repeat):
    for i in range(n):
      i = idxs.index(i)

      m = xs[i] % (n - 1)
      for (j, k) in zip(range(i, i + m), range(i + 1, i + m + 1)):
        j, k = j % n, k % n
        xs[j], xs[k] = xs[k], xs[j]
        idxs[j], idxs[k] = idxs[k], idxs[j]

  return xs


def grove_coordinates(xs: list[int]) -> tuple[int, ...]:
  n = len(xs)
  i = xs.index(0)
  return tuple(xs[(i + 1000 * offset) % n] for offset in [1, 2, 3])


def main(argv):
  xs = parse(_INPUT_FILE.value)

  # Part 1.
  print(sum(grove_coordinates(mixin(xs))))

  # Part 2.
  xs = [811589153 * x for x in xs]
  print(sum(grove_coordinates(mixin(xs, repeat=10))))


if __name__ == '__main__':
  app.run(main)
