#! /usr/bin/env python
# -*- coding: utf-8 -*-
# csv_grep - filter CSV files by column name using PCRE regular expressions
import sys, re, operator

concat = lambda z: reduce(operator.add, z)
match_fn = lambda (name,_): not any(match_attr.search(name) for match_attr in match_attrs)
cond_invert = lambda x:x
mode = 'regexp'
try:
    if sys.argv[1] == '-x':
        mode = 'index'
        del sys.argv[1]
        match_fn = lambda (_,idx): idx not in match_attrs
    elif sys.argv[1] == '-m':
        mode = 'exact-match'
        del sys.argv[1]
        match_fn = lambda (attr,_): attr not in match_attrs
    if sys.argv[1] == '-v':
        cond_invert = lambda x:not x
        del sys.argv[1]
    delim = sys.argv[1]

    match_attrs = sys.argv[2:]
    match_attrs[0]

    # Read these now since current negative index implementation needs the number of columns
    IdxAttrs = dict(enumerate(sys.stdin.readline().strip().split(delim)))
    Attrs = dict(((attr,idx),idx) for idx,attr in IdxAttrs.items())
    NumColumns = len(Attrs)
    if len(IdxAttrs) != len(set(IdxAttrs.values())):
        print >>sys.stderr, "Warning: Input contains duplicate column names"

    def safemod(x,y):
        if abs(x) >= y:
            print >>sys.stderr, "Warning: indices were wrapped around (requested attribute %d(%d) out of %d)" % (x,x%y,y)
        return x % y

    def get_indices(expr):
        X = re.split('[^-\d]+', expr)[:2]
        if len(X) == 1:
            return [ safemod(int(expr), len(Attrs)) ]
        if not X[0] and not X[1]:
            raise Exception("Invalid index or index range: '%s'" % expr)

        start = safemod( int(X[0]) if X[0] else 0, len(Attrs) )
        end = safemod( int(X[1]) if X[1] else len(Attrs)-1, len(Attrs) )
        return range(start, end+1)

    if mode == 'index':
        match_attrs = set(concat(map(get_indices, match_attrs)))
    elif mode == 'regexp':
        match_attrs = map(re.compile, match_attrs)

except IndexError:
    print "Usage: %s [-v] <delim> <column regexps ...>" % sys.argv[0]
    print "       %s -m [-v] <delim> <column names (exact match) ...>" % sys.argv[0]
    print "       %s -x [-v] <delim> <indices or index ranges, e.g. 3, 0:5, or -5..-2 ...>" % sys.argv[0]
    sys.exit(1)

for attr in Attrs.keys():
    if cond_invert(match_fn(attr)):
        idx = Attrs[attr]
        del IdxAttrs[idx]
        del Attrs[attr]

Order = sorted(IdxAttrs)
print delim.join(IdxAttrs[i] for i in Order)

for lineno,line in enumerate(sys.stdin,1):
    instance = line.strip().split(delim)
    row_length = len(instance)
    if row_length == NumColumns:
        print delim.join(instance[i] for i in Order)
    else:
        print >>sys.stderr, "Warning: Wrong number of columns: expected %d, got %d at line %d" % (NumColumns, row_length, lineno)
        print delim.join(instance[i] for i in Order if i<len(instance))
