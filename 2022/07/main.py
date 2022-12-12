import collections
import dataclasses
import re

from absl import app
from absl import flags
from typing import Sequence, Iterable, Optional

FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')


@dataclasses.dataclass(frozen=True)
class File:
  name: str
  size: int


class Dir():

  def __init__(self, name: str, parent: Optional['Dir'] = None):
    self.name = name
    self._parent = parent
    self._dirs = {}
    self._files = {}

  def cd(self, name) -> 'Dir':
    if name == '..':
      assert self._parent
      return self._parent

    if name not in self._dirs:
      self._dirs[name] = Dir(name, parent=self)
    return self._dirs[name]

  def add_file(self, f: File):
    self._files[f.name] = f

  @property
  def files(self) -> Sequence[File]:
    return list(self._files.values())

  @property
  def dirs(self) -> Sequence['Dir']:
    return list(self._dirs.values())

  @property
  def size(self) -> int:
    sz = 0
    for _, _, files in walk(self):
      sz += sum(f.size for f in files)
    return sz


def walk(d: Dir) -> Iterable[tuple[Dir, Sequence[Dir], Sequence[File]]]:
  yield (d, d.dirs, d.files)
  for d in d.dirs:
    yield from walk(d)


def parse(path: str) -> Dir:
  with open(path) as f:
    lines = f.read().splitlines()
  lines = lines[1:]  # First lines is always 'cd /'

  root = Dir('/')
  cur = root

  def is_cmd() -> bool:
    nonlocal lines
    return bool(lines) and (lines[0][0] == '$')

  def is_cd() -> bool:
    nonlocal lines
    return bool(lines) and bool(re.fullmatch(r'\$ cd .*', lines[0]))

  def is_ls() -> bool:
    nonlocal lines
    return bool(lines) and bool(re.fullmatch(r'\$ ls', lines[0]))

  def handle_cd():
    nonlocal lines, cur

    l, lines = lines[0], lines[1:]
    m = re.fullmatch(r'\$ cd (.+)', l)
    assert m

    (d,) = m.groups()
    cur = cur.cd(d)

  def handle_ls():
    nonlocal lines, cur
    assert is_ls()

    lines = lines[1:]
    while lines and not is_cmd():
      l, lines = lines[0], lines[1:]
      m = re.fullmatch(r"(\d+) (.*)", l)
      if m:
        sz, name = m.groups()
        cur.add_file(File(name=name, size=int(sz)))

  while lines:
    if is_cd():
      handle_cd()
    elif is_ls():
      handle_ls()

  return root


def main(argv):
  root = parse(_INPUT_FILE.value)

  free = 70000000 - root.size
  req_space = 30000000 - free

  tot_l1e5 = 0
  smallest_to_del = 1000000000000
  for r, _, _ in walk(root):
    sz = r.size

    if sz <= 1e5:
      tot_l1e5 += sz
    if sz >= req_space:
      smallest_to_del = min(smallest_to_del, sz)

  print(tot_l1e5)
  print(smallest_to_del)


if __name__ == '__main__':
  app.run(main)
