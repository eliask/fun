#! /usr/bin/env python
# -*- coding: utf-8 -*-
# splitpipe - execute a command every N lines of stdin input
import sys
from subprocess import Popen, PIPE

if not sys.argv[2:]:
    print "Usage: %s [-q] <period (e.g. 5000)> command ..." % sys.argv[0]
    sys.exit(1)

quiet = False
if sys.argv[1] == '-q':
    quiet = True
    del sys.argv[1]

N = int(sys.argv[1])
cmd = sys.argv[2:]
process = None

for i, line in enumerate(sys.stdin):
    if i % N == 0:
        if not quiet:
            print >>sys.stderr, "splitpipe: Starting a new process at %d lines" % i
        if process:
            process.stdin.close()
            process.wait()
        process = Popen(cmd, stdin=PIPE)

    process.stdin.write(line)
