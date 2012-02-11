#! /usr/bin/env python
# -*- coding: utf-8 -*-
# widefmt - like fmt -w N for large N; joins together all text between empty lines
import sys, re

re_split = re.compile('^\s*$')
out = ''
for line in sys.stdin:
    L = line.strip()
    if re_split.match(line):
        print out
        out = L
    else:
        out += ' '+L if out else L

if out: print out
