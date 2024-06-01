import sys

from .core import build


def buildc():
    build(sys.argv[1:])


def buildcpp():
    build(sys.argv[1:], True)
