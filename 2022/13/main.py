from absl import app
from absl import flags
from typing import Sequence, Union

import functools
import math

FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')

Packet = Union[int, Sequence['Packet']]


def parse(path: str) -> Sequence[Packet]:
  with open(path) as f:
    lines = f.read().splitlines()
  return [eval(l) for l in lines if l != '']


def cmp(p0: Packet, p1: Packet):
  """Compares packets `p0` and `p1`.

  Returns a negative number, zero, or positive number if `p0` is considered less,
  equal, or greater than `p1` respectively.
  """
  if isinstance(p0, int) and isinstance(p1, int):
    return p0 - p1

  if isinstance(p0, int):
    return cmp([p0], p1)

  if isinstance(p1, int):
    return cmp(p0, [p1])

  for (x, y) in zip(p0, p1):
    v = cmp(x, y)
    if v != 0:
      return v

  return len(p0) - len(p1)


def main(argv):
  pkts = parse(_INPUT_FILE.value)

  # Part 1.
  pkt_pairs = zip(pkts[::2], pkts[1::2])
  count = 0
  for i, (p0, p1) in enumerate(pkt_pairs):
    if cmp(p0, p1) <= 0:
      count += (i + 1)
  print(count)

  # Part 2.
  DIVIDER_PACKETS = ([[[2]], [[6]]])

  pkts.extend(DIVIDER_PACKETS)
  pkts = sorted(pkts, key=functools.cmp_to_key(cmp))

  decoder_key = math.prod(
      [i + 1 for i, pkt in enumerate(pkts) if pkt in DIVIDER_PACKETS])
  print(decoder_key)


if __name__ == '__main__':
  app.run(main)
