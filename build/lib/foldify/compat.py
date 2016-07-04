import sys

if sys.version_info < (3, 0):
    # sys.stdout.write("Sorry, requires Python 3.x, not Python 2.x\n")
    # sys.exit(1)
    # Implement handling for python 2
    input = raw_input
else:
    input = input
