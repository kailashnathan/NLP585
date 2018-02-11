# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from pprint import pprint
grammar_text ="""
S -> NP VP   0.8
S -> Aux_NP VP   0.1
Aux_NP -> Aux NP  1
S -> book  0.01
S -> include  0.004
S -> prefer  0.006
S -> Verb NP  0.05
S -> VP PP  0.03
NP -> I    0.1
NP -> he    0.02
NP -> she    0.02
NP -> me    0.06
NP -> Houston    0.16
NP -> NWA    0.04
NP -> Det Nominal    0.6
Nominal -> book    0.03
Nominal -> flight    0.15
Nominal -> meal    0.06
Nominal -> money    0.06
Nominal -> Nominal Noun  0.2
Nominal -> Nominal PP    0.5
VP -> book    0.1
VP -> include    0.04
VP -> prefer    0.06
VP -> Verb NP    0.5
VP -> VP PP  0.3
PP -> Prep NP    1.0
Det -> the   0.6
Det ->  a    0.2
Det -> that  0.1
Det -> this  0.1
Noun -> book 0.1
Noun -> flight   0.5
Noun -> meal 0.2
Noun -> money    0.2
Verb -> book 0.5
Verb -> include  0.2
Verb -> prefer   0.3
Pronoun -> I 0.5
Pronoun -> he    0.1
Pronoun -> she   0.1
Pronoun -> me    0.3
Proper-Noun -> Houston   0.8
Proper-Noun -> NWA   0.2
Aux -> does  1.0
Prep -> from 0.25
Prep -> to   0.25
Prep -> on   0.1
Prep -> near 0.2
Prep -> through  0.2
"""
p=[]
grammar_rules = []
lexicon = {}
probabilities = {}
possible_parents_for_children = {}
i=0
children=[]
leftlist=[]
rightlist=[]
i=0
for line in grammar_text.strip().split("\n"):
    if not line.strip(): continue
    left, right = line.split("->")
    #print left,right
    leftlist.append(left.strip())
    #right=(right.strip().split())
    rightlist.append(right.strip().split())
    #print rightlist
    p.append(rightlist[-1])
    
    children.append(rightlist[i][:-1])
    i+=1    
    
xc=[]
xd=[]   
c=[]
d=[]
for i in range(len(children)):
    xc.append(p[i])
    xd.append(leftlist[i])
    if len(children[i])==1:
        c.append(children[i])
        d.append(leftlist[i])
    else:
        rule = (leftlist[i], tuple(children[i]))
        grammar_rules.append(rule)

for i in range(len(c)):
    if d[i] not in lexicon:
        lexicon[d[i]] = []
    lexicon[d[i]].append(c[i])
    
for i in range(len(xc)):
    if xd[i] not in probabilities:
        probabilities[xd[i]] = []
    probabilities[xd[i]].append(xc[i])        


#pprint(grammar_rules)

possible_parents_for_children = {}
for parent, (leftchild, rightchild) in grammar_rules:
    if (leftchild, rightchild) not in possible_parents_for_children:
        possible_parents_for_children[leftchild, rightchild] = []
    possible_parents_for_children[leftchild, rightchild].append(parent)
pprint(possible_parents_for_children)
def populate_grammar_rules():
    global grammar_rules, lexicon, probabilities, possible_parents_for_children
    # TODO Fill in your implementation for processing the grammar rules.
    pass
    print "Grammar rules in tuple form:"
    pprint(grammar_rules)
    print '\n\n'
    print "Rule parents indexed by children:"
    pprint(possible_parents_for_children)
    print '\n\n'
    print "probabilities"
    pprint(probabilities)
    print '\n\n'
    print "Lexicon"
    pprint(lexicon)


def pcky_parse(sentence):
    # Return the most probable legal parse for the sentence
    # If nothing is legal, return None.
    # This will be similar to cky_parse(), except with probabilities.
    global grammar_rules, lexicon, probabilities, possible_parents_for_children
    # TODO complete the implementation
    
    
    
    
    global grammar_rules, lexicon

    N = len(sentence)
    cells = {}
    for i in range(N):
        for j in range(i + 1, N + 1):
            cells[(i, j)] = []


    for j in range(0,N):
        t = ""
        if sentence[j] in lexicon['Noun']:
            t = 'Noun'
        if sentence[j] in lexicon['S']:
            t = 'S' 
        if sentence[j] in lexicon['VP']:
            t = 'VP'     
        if sentence[j] in lexicon['Verb']:
            t = 'Verb'
        if sentence[j] in lexicon['Prep']:
            t = 'Prep'
        if sentence[j] in lexicon['Det']:
            t = 'Det'
        if sentence[j] in lexicon['Pronoun']:
            t = 'Pronoun'

        cells[j,j+1] = [t, sentence[j]]

    diff = 1
    for i in range(1,N+1):
        diff = diff+1
        for j in range(0,N-diff+1):
             #k= diff + k
            i1 = j
            j1 = j+diff
            for k in range(i1+1,j1):
                if (i1,k) in cells.keys() and (k,j1) in cells.keys():
                     #print "present"
                    for b in cells[i1,k]:
                        for c in cells[k,j1]:
                            if((b,c) in possible_parents_for_children.keys()):
                                 #print "parsing",b,c
                                cells[i1,j1] = possible_parents_for_children[b,c]
                                cells[i1,j1].append([k,b,c])
                                 #cells[i,j].extend([b])
                                 #cells[i,j].extend([c])
     # TODO replace the below with an implementation
    pprint(cells)

    if('S' in cells[0,N]):
         #call backprob.
        

        backprob(cells,0,N)
        print "\n"
        return True
    else:
        print "\n"
        return None

def backprob(cells,i,j):
    tag = cells[i,j][0]
    print "["+tag,


    if(type(cells[i,j][1])==str):
        print cells[i,j][1] + "]",
        return
    else:
        for x in cells[i,j][1:]:
             #print x
            k = x[0]
            if((i,k) in cells.keys() and (k,j) in cells.keys()):
                if(cells[i,k] != [] and cells[k,j]!=[]):
                    backprob(cells,i,k)
                    print "]",
                    backprob(cells,k,j)
                    print "]",
                    break;



