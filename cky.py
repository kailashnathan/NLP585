from pprint import pprint

# The productions rules have to be binarized.

grammar_text = """
S -> NP VP
NP -> Det Noun
VP -> Verb NP
PP -> Prep NP
NP -> NP PP
VP -> VP PP

S -> NPS VPS


NPS ->Det Nouns


VPS ->Verbs NPS  


VPS ->Verbs NP 


PP ->Prep NPS


NPS ->NPS PP


VPS -> VPS PP
"""

lexicon = {
    'Noun': set(['cat', 'dog', 'table', 'food']),
    'Verb': set(['attacked', 'saw', 'loved', 'hated','attacks']),
    'Prep': set(['in', 'of', 'on', 'with']),
    'Det': set(['the', 'a']),
    'Nouns':set(['cats','dogs']),
    
    
    'Verbs':set(['attack']),
}

# Process the grammar rules.  You should not have to change this.
grammar_rules = []
for line in grammar_text.strip().split("\n"):
    if not line.strip(): continue
    left, right = line.split("->")
    left = left.strip()
    children = right.split()
    rule = (left, tuple(children))
    grammar_rules.append(rule)
possible_parents_for_children = {}
for parent, (leftchild, rightchild) in grammar_rules:
    if (leftchild, rightchild) not in possible_parents_for_children:
        possible_parents_for_children[leftchild, rightchild] = []
    possible_parents_for_children[leftchild, rightchild].append(parent)
# Error checking
all_parents = set(x[0] for x in grammar_rules) | set(lexicon.keys())
for par, (leftchild, rightchild) in grammar_rules:
    if leftchild not in all_parents:
        assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % leftchild
    if rightchild not in all_parents:
        assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % rightchild

# print "Grammar rules in tuple form:"
# pprint(grammar_rules)
# print "Rule parents indexed by children:"
# pprint(possible_parents_for_children)





    
def assign(wo):
    global lexicon
    
    x=len(wo)
    word=wo[2:x-2]
    if word in lexicon['Noun']:
        return 'Noun'
    elif word in lexicon['Nouns']:
        return 'Nouns'
    elif word in lexicon['Verb']:
        return 'Verb'
    elif word in lexicon['Verbs']:
        return 'Verbs'
    elif word in lexicon['Prep']:
        return 'Prep'
    elif word in lexicon['Det']:
        return 'Det'    
def cky_acceptance(sentence):
    # return True or False depending whether the sentence is parseable by the grammar.
    global grammar_rules, lexicon

    # Set up the cells data structure.
    # It is intended that the cell indexed by (i,j)
    # refers to the span, in python notation, sentence[i:j],
    # which is start-inclusive, end-exclusive, which means it includes tokens
    # at indexes i, i+1, ... j-1.
    # So sentence[3:4] is the 3rd word, and sentence[3:6] is a 3-length phrase,
    # at indexes 3, 4, and 5.
    # Each cell would then contain a list of possible nonterminal symbols for that span.
    # If you want, feel free to use a totally different data structure.
    N = len(sentence)
    cells = {}
    for i in range(N):
        for j in range(i + 1, N + 1):
            cells[(i, j)] = []
    #pprint(cells)      
    for i in range(N):
        j=i+1
        cells[(i,j)]=assign(str(sentence[i:j]))
        
    for cvc in range(N):
        for i in range(N):
            for j in range(1,N+1):
                for k in range(i+1,j-1+1):
                    d=j-i-1
                    if True:
                   # if (((abs(j-k))==d) and(abs((k-i))==d)):
                   # print "R",k,j
                   # print "L",i,k
                   # print "cell",i,j
                   # print " "
                
                   
                        b=cells[i,k]
                        #print b
                        c=cells[k,j]
                        #print c
                    
               
                        if (b,c) in possible_parents_for_children.keys():
                        
                            a=possible_parents_for_children[b,c]
                            #print "ans",a[0]
                          #  print type(b),type(a[0])
                    
                            cells[i,j]=a[0]
                
               
       
                
            #if cell[k,j]
            #b=cells[k,j]
            #c=cells[k,j+1]
            #print b,c

    # TODO replace the below with an implementation
    pprint(cells)
    for i in range(N):
        for j in range(i + 1, N + 1):
            
            if 'S' in cells.values():
               # print "ASDas"
                return True
            else:
              #  print "AS"
                return False


def cky_parse(sentence):
    
    
    
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
        elif sentence[j] in lexicon['Nouns']:
            t = 'Nouns' 
        elif sentence[j] in lexicon['Verbs']:
            t = 'Verbs'     
        elif sentence[j] in lexicon['Verb']:
            t = 'Verb'
        elif sentence[j] in lexicon['Prep']:
            t = 'Prep'
        elif sentence[j] in lexicon['Det']:
            t = 'Det'
           

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
