import parse
import json
import sys

with open(sys.argv[1]) as f:
    parse.Parser(f.read())