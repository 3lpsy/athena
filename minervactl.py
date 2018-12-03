#!/usr/bin/env python

from sys import exit
from minerva.cli import make_cli
if __name__ == '__main__':
    exit(make_cli("manager").run())
