import wordfreq, random, sys
seed=int(sys.argv[1]) if len(sys.argv)>1 else 1
random.seed(seed)
top=[w for w in wordfreq.top_n_list('en',12000) if w.isalpha() and w.isascii()]
import os
bad=set(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"crossword_bad_words.txt")).read().split())
W4=[w.upper() for w in top if len(w)==4 and w not in bad]
W5=[w.upper() for w in top if len(w)==5]
S4=set(W4);S5=set(W5)
from collections import defaultdict
def prefixes(ws):
    p=set()
    for w in ws:
        for i in range(len(w)+1): p.add(w[:i])
    return p
P4=prefixes(W4);P5=prefixes(W5)
# grid 5x5, black (0,0),(4,4)
def colstr(rows,c):
    s=''
    for r,row in enumerate(rows):
        if (r,c) in ((0,0),(4,4)): continue
        s+=row[c]
    return s
def ok(rows):
    for c in range(5):
        s=colstr([ (' '+rows[0]) if i==0 else (rows[i]+' ' if i==4 else rows[i]) for i in range(len(rows))],c).replace(' ','')
        full = 4 if c in (0,4) else 5
        P = P4 if full==4 else P5
        if s not in P: return False
    return True
def build(rows):
    i=len(rows)
    if i==5: return rows
    cand = W4 if i in (0,4) else W5
    cand=cand[:]; random.shuffle(cand)
    for w in cand:
        if w in rows: continue
        nr=rows+[w]
        if ok(nr):
            r=build(nr)
            if r: return r
    return None
r=build([])
print(r)
