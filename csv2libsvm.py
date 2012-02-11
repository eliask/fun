#! /usr/bin/env python
# -*- coding: utf-8 -*-
# csv2libsvm - Convert CSV files to LibSVM format
import sys, re

try:
    delim = sys.argv[1]
except IndexError:
    print "Usage: %s <delim>" % sys.argv[0]
    sys.exit(1)

sys.stdin.readline() # No use for the header
for line in sys.stdin:
    instance = line.strip().split(delim)
    # Make sure the target value is known:
    if instance[-1] not in ('', '?'):
        print ' '.join([instance[-1]]+['%d:%s'%(i,x) for i,x in enumerate(instance[:-1],1) if x not in ('', '?')])
