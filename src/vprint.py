import sys
import os

verboseMatch = []
helpMatch = []


for x in sys.argv:
    verboseMatch.append(x.lower() in ["-v", "--verbose"])
    helpMatch.append(x.lower() in ["-h", "--help"])


"""Create help menu"""
if any(helpMatch):
    print("use \"-v or --verbose\" for verbose\nuse \"-p or --path\" followed by a valid path to save data to that file")

"""Create verbose function. Essentially just a print with a toggle"""
if any(verboseMatch):
    vprint = print
else:
    vprint = lambda *a, **k: None
