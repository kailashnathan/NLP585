# -*- coding: utf-8 -*-
"""
Created on Thu Nov 09 13:03:01 2017

@author: Kailash Nathan
"""

from __future__ import division
import os
clear = lambda: os.system('cls')
clear()

import collections
import matplotlib.pyplot as plt
import math
import os
import time
from stop_words import get_stop_words
import numpy as np
import glob
psl= ["good", "nice", "love", "excellent", "fortunate", "correct", "superior"]
nsl=["bad", "nasty", "poor", "hate", "unfortunate", "wrong", "inferior"]
el=['@','#','.']
f=open('tweets.txt','r')

a=[]
c=[]
d=[]
i=0
for line in f:
    a.append(line)
    c.append(line)
b=a[:99]
f.close()
d=a[:100]

posd= collections. defaultdict(float)
negd = collections.defaultdict(float)
wc=collections.defaultdict(float)
# word count uniquue per tweet using set
notw=0 # no of tweets
f=open('tweets.txt','r')
xc=0   
for line in a:
     notw+=1   
     uw= set(line.split())
     for w in uw:
         if w not in (psl or nsl)and w[0] not in el:
             wc[w]+=1
             xc+=1
    
#print wc
#print "No of tweets",notw

cg=0
cn=[]
i=0
def countofyg(b,ll):
    #global cg
    cg = 0
    
    for line in b:
        
        uw=set(line.split())
        #print uw
        flag=1   
        for w in uw :
            #print w
            if (w in ll) and flag:
                cg+=1
                flag=0
                
    return cg


#print "CG",cg
'''     
print "tweets with +ve words",countofyg(a,psl)
print "Tweets with -ve words",countofyg(a,nsl)
print "Intersection",countofyg(a,psl+nsl)
'''
np=countofyg(a,psl)
nn=countofyg(a,nsl)
def pxy(line,llist,dd):
    for word in line.split():
        #print word
        if word not in (llist) or word[0] not in el:
            count=0
           # print word
           
            for w in line.lower().split():
                flag=1
              #  print w
                
                
                if (w in llist) and flag:
                      
                      count=1
                      flag=0
                      
                #    print w
            dd[word]+=count
            
for line in a:
   pxy(line.lower(),psl,posd)
    
for line in a:
    pxy(line.lower(),nsl,negd)

#pxy("i hate you now ",nsl,negd)          
        
#print "no of tweets with neg words next to the word now",negd['is']
#print "no of tweets with pos words next to the word now",posd['is']          
'''
for line in a:
    for word in line:
        if wc[word]==0:
            print word
'''
pmi=collections.defaultdict(float)
for line in a:
    for word in line.split():
        if word not in (psl and nsl) and word[0] not in el:
            #print word,posd[word],notw,np,wc[word]
            if wc[word]>0:
                x1=((posd[word]* notw)/(float(np) * wc[word]))
                if x1!=0:
                    lx1=math.log(x1)
                else:
                    lx1=0
                x2=((negd[word]* notw)/(float(nn) * wc[word]))
                if x2!=0:
                    lx2=math.log(x2)
                else:
                    lx2=0
                pmi[word]=lx1-lx2
def top50():                  
#Answer to Question 2            
    print "top 50 positive polarity words",sorted(pmi.items(), key=lambda(k,v): v, reverse=True)[:50]
    print "\n\n"
    print "top 50 negative polarity words",sorted(pmi.items(), key=lambda(k,v): v)[:50]
    print "\n\n"
#Answer for Question 3 
pmi2=collections.defaultdict(float)
    
for line in a:
    for word in line.split():
        if word not in (psl and nsl) and word[0] not in el:
            #print word,posd[word],notw,np,wc[word]
            if wc[word]>500:
                x1=((posd[word]* notw)/(float(np) * wc[word]))
                if x1!=0:
                    lx1=math.log(x1)
                else:
                    lx1=0
                x2=((negd[word]* notw)/(float(nn) * wc[word]))
                if x2!=0:
                    lx2=math.log(x2)
                else:
                    lx2=0
                pmi2[word]=lx1-lx2
def top50withcount():    
    print "top 50 positive polarity words",sorted(pmi2.items(), key=lambda(k,v): v, reverse=True)[:50]
    print "\n\n"
    print "top 50 negative polarity words",sorted(pmi2.items(), key=lambda(k,v): v)[:50]        
        