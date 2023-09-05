import os
import sys

command = sys.argv[1]
values = sys.argv[2:]

for value in values:
    x = os.system(command + " " + value)
    print(x)

