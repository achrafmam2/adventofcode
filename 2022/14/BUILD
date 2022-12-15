load("@rules_python//python:defs.bzl", "py_binary")
load("@pypi//:requirements.bzl", "requirement")


py_binary(
  name = "main",
  srcs = ["main.py"],
  deps = [
    requirement("absl-py"),
    requirement("numpy"),
  ],
)
