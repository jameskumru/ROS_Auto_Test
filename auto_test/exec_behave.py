#!/usr/bin/env python

from subprocess import Popen, PIPE
import sys

cmd = "behave"

iterargs = iter(sys.argv)
next(iterargs)
for arg in iterargs:
    cmd = "{command} {argument}".format(command=cmd, argument=str(arg))

p = Popen(cmd, stdout=PIPE, executable="/bin/bash", shell=True)
out, err = p.communicate()

print(out)
print(err)