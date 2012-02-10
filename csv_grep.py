#! /usr/bin/env python
# -*- coding: utf-8 -*-
# csv_grep - filter CSV files by column name using PCRE regular expressions
import sys, re

cond_invert = lambda x:x
try:
    if sys.argv[1] == '-v':
        cond_invert = lambda x:not x
        del sys.argv[1]
    delim = sys.argv[1]
    re_attrs = sys.argv[2:]
    re_attrs[0]
except IndexError:
    print "Usage: %s [-v] <delim> <column regexps...>" % sys.argv[0]
    sys.exit(1)

IdxAttrs = dict(enumerate(sys.stdin.readline().strip().split(delim)))
Attrs = dict((attr,idx) for idx,attr in IdxAttrs.items())

for attr in Attrs.keys():
    if cond_invert(not any(re.search(re_attr, attr) for re_attr in re_attrs)):
        idx = Attrs[attr]
        del IdxAttrs[idx]
        del Attrs[attr]

Order = sorted(IdxAttrs)
print delim.join(IdxAttrs[i] for i in Order)

for line in sys.stdin:
    instance = line.strip().split(delim)
    print delim.join(instance[i] for i in Order)
