#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Markov chain sentence generator.

Usage: python markov.py [arg]

if the argument is specified, the Markov chains are read from the store file and a few sentences are generated to stdout.
Otherwise training data is read from stdin and saved to the Markov
chains are saved to the store file.

To use this in other code, do something like:
import markov
chain = markov.read()
print markov.generate(chain)
print markov.generate(chain, ['word','argument','example'])
"""
import sys, os, cPickle, random
StoreFile=os.environ['HOME']+'/.markov-store'
NGRAM=2

def add_word(chain, _state, word):
    assert type(word) != list, word
    assert len(_state) >= 1, _state
    if word is not None:
        word = word.strip().lower()

    for x in range(len(_state)):
        add_ngram_word(chain, _state[x:], word)

    if word is None:
        _state[:] = [None]
    else:
        _state.append(word)
        if len(_state) > NGRAM: del _state[0]

def add_ngram_word(chain, _state, word):
    state = tuple(_state)
    if not state in chain:
        chain[state]={}
    if not word in chain[state]:
        chain[state][word] = 1
    else:
        chain[state][word] += 1

def train_line(chain, line):
    fwd, inv = chain
    sents = line.split('. ')
    fstate=[None]
    for sent in sents:
        words = sent.split()
        map(lambda x:add_word(fwd,fstate,x), words)
    add_word(fwd,fstate,None)

    istate=[None]
    sents.reverse()
    for sent in sents:
        words = sent.split()
        words.reverse()
        map(lambda x:add_word(inv,istate,x), words)
        add_word(inv,istate,None)

def train_file(h):
    chain = [{},{}]
    for line in h.readlines():
        train_line(chain, line)

    w = open(StoreFile, 'w')
    cPickle.dump(chain, w, -1)
    w.close()
    return chain

def weighted_selection(items, total):
    x = total * random.random()
    for i, w in items:
        x -= w
        if x < 0: return i

def generate(chain, words=[]):

    def test_continuations(words):
        N = min(len(words), NGRAM)
        fwd_chain, inv_chain = chain
        fwd_state = tuple(words[-N:])
        inv_state = tuple(words[:N])
        return fwd_state in fwd_chain, \
               inv_state in inv_chain

    def recurse(words, limit):
        if limit == 0: return generate2(chain, [])
        X = min(limit, len(words))
        W = [ words[i:i+X] for i in range( len(words)-X+1 ) ]
        C = map(test_continuations, W)
        p1 = map(lambda (F,I):F and I, C)
        p2 = map(lambda (F,I):F, C)
        p3 = map(lambda (F,I):I, C)

        for p,dir in zip( (p1,p2,p3), (0,1,-1) ):
            sols = [ w for w,t in zip(W,p) if t ]
            #print "dir:%d, "%dir, zip(W,p)
            if sols:
                words = random.sample(sols, 1)[0]
                return generate2(chain, words, dir)
        return recurse(words, limit-1)

    words = map(lambda x:x.lower(), words)
    return recurse( words, 3 )

def generate2(chain, words=[], dir=0):
    # dir=0: both; dir>0: forward; dir<0: backward

    fwd_chain, inv_chain = chain
    state = [None]
    if words:
        state = (state+words)[-NGRAM:]
        if tuple(state) in fwd_chain:
            total = sum( fwd_chain[tuple(state)].values() )
        else:
            total = 0
        prob = 1 - min(1, 1/4.*(total-1))
        # If there are few instances of the context, fall
        # back to using smaller N-grams:
        if random.random() <= prob:
            del state[0]

    fwd = fwd_chain, state[-NGRAM:]
    inv = inv_chain, state[:NGRAM]

    res = [] + words
    if words and dir <= 0:
        word = generate_one(inv)
        #print "backward", inv[1], word
        while word is not None:
            res.insert(0, word)
            word = generate_one(inv)

    if dir >= 0:
        word = generate_one(fwd)
        #print "forward", fwd[1], word
        while word is not None:
            res.append(word)
            word = generate_one(fwd)

    return ' '.join(res)

def generate_one((chain, _state), items=None):
    state = tuple(_state)

    if not state in chain:
        if len(state) > 1:
            return generate_one((chain,_state[1:]), items)
        state2 = random.sample(chain.keys(), 1)[0]
        word = random.sample(chain[state2].keys(), 1)[0]
    else:
        total = sum( chain[state].values() )
        word = weighted_selection( chain[state].items(), total )

    if word is None:
        _state[:] = [None]
    else:
        _state.append(word)
        if len(_state) > NGRAM: del _state[0]
    return word

def read():
    print "Reading store file..."
    h = open(StoreFile,'r')
    chain = cPickle.load(h)
    print "FWD:%d INV:%d" % (len(chain[0]), len(chain[1]))
    return chain

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Training..."
        chain = train_file(sys.stdin)
    else:
        chain = read()

    print "Generating..."
    for _ in range(3):
        print ">>>",generate(chain, ['count'])
