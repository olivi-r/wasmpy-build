import sys

from .core import buildc as _buildc, buildcpp as _buildcpp


def buildc():
    _buildc(sys.argv[1:])


def buildcpp():
    _buildcpp(sys.argv[1:])
