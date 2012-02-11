#! /usr/bin/env python
# -*- coding: utf-8 -*-
# csv_grep - filter CSV files by column name using PCRE regular expressions
import sys, re, operator

concat = lambda z: reduce(operator.add, z)
match_fn = lambda attr: not any(re.search(match_attr, attr) for match_attr in match_attrs)
cond_invert = lambda x:x
mode = 'regexp'
try:
    if sys.argv[1] == '-x':
        mode = 'index'
        del sys.argv[1]
        match_fn = lambda attr: Attrs[attr] not in match_attrs
    if sys.argv[1] == '-v':
        cond_invert = lambda x:not x
        del sys.argv[1]
    delim = sys.argv[1]

    match_attrs = sys.argv[2:]
    match_attrs[0]

    # Read these now since current negative index implementation needs the number of columns
    IdxAttrs = dict(enumerate(sys.stdin.readline().strip().split(delim)))
    Attrs = dict((attr,idx) for idx,attr in IdxAttrs.items())

    if mode == 'index':
        match_attrs = set(concat((lambda x:range(x[0],1+x[1] if x[1:] else 1+x[0]))
                                 (map(lambda x:int(x)%len(Attrs),re.split('[^-\d]+',z)[:2]))
                                 for z in match_attrs))

except IndexError:
    print "Usage: %s [-v] <delim> <column regexps ...>" % sys.argv[0]
    print "       %s -x [-v] <delim> <index ranges, e.g. 0:5 or -5..-2 ...>" % sys.argv[0]
    sys.exit(1)

for attr in Attrs.keys():
    if cond_invert(match_fn(attr)):
        idx = Attrs[attr]
        del IdxAttrs[idx]
        del Attrs[attr]

Order = sorted(IdxAttrs)
print delim.join(IdxAttrs[i] for i in Order)

for line in sys.stdin:
    instance = line.strip().split(delim)
    print delim.join(instance[i] for i in Order)
