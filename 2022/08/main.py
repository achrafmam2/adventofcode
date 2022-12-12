from absl import app
from absl import flags

import numpy as np

FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')


def parse(path: str) -> np.ndarray:
  with open(path, 'r') as f:
    lines = f.read().splitlines()

  n, m = len(lines), len(lines[0])
  ts = np.zeros([n, m], dtype=np.int32)
  for i in range(n):
    for j in range(m):
      ts[i, j] = int(lines[i][j])

  return ts


def visible_trees(ts: np.ndarray) -> int:
  n, m = ts.shape
  count = 2 * (n + m) - 4  # Edges are always visible.
  for i in range(1, n - 1):
    for j in range(1, m - 1):
      # Find the tallest trees on the left, right, up and down
      # of the (i,j)th tree.
      ms = np.array([
          np.amax(ts[i, :j]),
          np.amax(ts[i, j + 1:]),
          np.amax(ts[:i, j]),
          np.amax(ts[i + 1:, j]),
      ])
      if any(ms < ts[i, j]):
        count += 1
  return count


def count_until(a: np.ndarray) -> int:
  """Keeps counting until the first non-zero element is found."""
  a = np.array(a, dtype=bool)
  if np.all(a == False):
    return a.size
  return np.argmax(a) + 1


def scenic_score(ts: np.ndarray) -> int:
  best = 0
  n, m = ts.shape
  for i in range(1, n - 1):
    for j in range(1, m - 1):
      t = ts[i, j]
      cs = np.array([
          count_until(ts[i, j - 1::-1] >= t),
          count_until(ts[i, j + 1:] >= t),
          count_until(ts[i - 1::-1, j] >= t),
          count_until(ts[i + 1:, j] >= t),
      ])
      best = max(best, np.prod(cs))
  return best


def main(argv):
  ts = parse(_INPUT_FILE.value)

  print(visible_trees(ts))
  print(scenic_score(ts))


if __name__ == '__main__':
  app.run(main)
