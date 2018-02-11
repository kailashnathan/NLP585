from __future__ import division
import sys,json,math
import os
import numpy as np
import math
import collections
def load_word2vec(filename):
    # Returns a dict containing a {word: numpy array for a dense word vector} mapping.
    # It loads everything into memory.
    
    w2vec={}
    with open(filename,"r") as f_in:
        for line in f_in:
            line_split=line.replace("\n","").split()
            w=line_split[0]
            vec=np.array([float(x) for x in line_split[1:]])
            w2vec[w]=vec
    return w2vec

def load_contexts(filename):
    # Returns a dict containing a {word: contextcount} mapping.
    # It loads everything into memory.

    data = {}
    for word,ccdict in stream_contexts(filename):
        data[word] = ccdict
    print "file %s has contexts for %s words" % (filename, len(data))
    return data

def cosinesim(a,b):
    #keys_a = set(a.keys())
    #keys_b = set(b.keys())
    #intersection = keys_a & keys_b
    #print intersection
    #print len(intersection)
    num=0
    d1=0
    d2=0
    for i,j in a.items():
        d1+=(a[i]*a[i])
        if i in b:
            num+=a[i]*b[i]
    for i,j in b.items():
        d2+=(b[i]*b[i])
          
    c1=math.sqrt(d1)
    c2=math.sqrt(d2)
    
    xc=c1*c2
    return num/xc

def coswordvec(a,b):
    x=np.dot(a,b)
    an= np.linalg.norm(a)
    bn=np.linalg.norm(b)
    return x/(an*bn)
    
#word_to_ccdict = load_contexts("nytcounts.4k")    

def cosines(a,b):
        
        wc=collections.defaultdict(float)
        for ke in word_to_ccdict.keys():
            if ke!=b:
                
                wc[ke]=cosinesim(a,word_to_ccdict[ke])
       
        #print wc     
        print sorted(wc.items(), key=lambda(k,v): v, reverse=True)[:50]
    
    
def stream_contexts(filename):
    # Streams through (word, countextcount) pairs.
    # Does NOT load everything at once.
    # This is a Python generator, not a normal function.
    for line in open(filename):
        word, n, ccdict = line.split("\t")
        n = int(n)
        ccdict = json.loads(ccdict)
        yield word, ccdict