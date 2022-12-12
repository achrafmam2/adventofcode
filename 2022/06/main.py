from absl import app
from absl import flags
from typing import Sequence

FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')


def parse(path: str) -> str:
  with open(path, 'r') as f:
    [msg] = f.read().splitlines()
    return msg


def main(argv):
  msg = parse(_INPUT_FILE.value)

  def first_marker(submsg_len: int):
    n = submsg_len
    return next(i + n for i in range(len(msg)) if len(set(msg[i:i + n])) == n)

  packet_marker = first_marker(4)
  msg_marker = first_marker(14)

  print(packet_marker, msg_marker)


if __name__ == '__main__':
  app.run(main)
