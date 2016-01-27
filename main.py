#%pylab inline
#sys.stdout = open('/dev/stdout', 'w')

#!/usr/bin/env python

import sys
import copy
import networkx as nx
import matplotlib.pyplot as plt
import networkx.algorithms.isomorphism as iso
from itertools import chain, combinations

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def Cache2Graph(c):
    Graph = nx.DiGraph()
    for line in c:
        p = line.split(',')
        f_id    = int(p[0])
        f_label = p[1].strip()
        t_id    = int(p[2])
        t_label = p[3].strip()
        relation = p[4].strip()
        if f_id not in Graph:
            Graph.add_node(f_id, name=f_label)
        if t_id not in Graph:
            Graph.add_node(t_id, name=t_label)
        Graph.add_edge(f_id ,t_id)

    #labels=dict((n,d['name']) for n,d in Graph.nodes(data=True)) 
    #nx.draw(Graph, labels=labels,node_size=1000, node_color='b')
    #plt.show()
    return Graph

def File2Graph():
    gList = []
    Cache = list()
    
    f = open("./input_1.in","r")
    while True:
        line = f.readline()
        if not line:
            break
        if not line.strip():
            if [] == Cache:
                continue
            g = Cache2Graph(Cache)
            gList.append(g)

            Cache = list()
            continue
        Cache.append(line)
    return gList

def gList2gDict(gList):
    r = dict()
    for i, o in zip(range(len(gList)), gList):
        r[i] = dict()
        r[i]['origin'] = o
    return r


suspicious = list()
index = 0

def isomorphism_set(sg):
    for s in suspicious:
        GM = nx.isomorphism.DiGraphMatcher(sg, s)
        if GM.is_isomorphic():
            return True
    return False

def supportValue(gList, sg):
    print '*** start ***'
    v = 0
    sptList = []
    for i in range(len(gList)):
        g = gList[i]
        GM = nx.isomorphism.DiGraphMatcher(g, sg, node_match=iso.categorical_node_match('name', None))
        if GM.subgraph_is_isomorphic():
            v += 1
            sptList.append(i)
    print '*** end.. ***'
    return v, sptList

def main(seed_number, minspt):
    global index
    global suspicious
    
    gList = File2Graph()
    g_seed = gList[seed_number]
    
    somelist = [x for x in powerset(g_seed.nodes()) if len(x) > 1]

    while True:
        if [] == somelist:
            break
        nodesGroup = somelist.pop(0)
        print "$$ total: ", len(somelist), nodesGroup
        
        sg = g_seed.subgraph(nodesGroup)
        '''
        labels=dict((n,d['name']) for n,d in sg.nodes(data=True)) 
        nx.draw(sg, labels=labels,node_size=1000)
        plt.show()
        raw_input()
        '''
        spt, sptList = supportValue(gList, sg)
        if spt >= minspt:
            info = '-'.join(str(i) for i in sptList)
            '''
            for s in suspicious:
                GM = nx.isomorphism.DiGraphMatcher(sg, s)
                GM.is_isomorphic()
                apd = 0
                break
                '''
            if not isomorphism_set(sg):
                suspicious.append(sg)
                ##

                labels=dict((n,d['name']) for n,d in sg.nodes(data=True)) 
                nx.draw(sg, labels=labels,node_size=1000)
                #plt.show()

                #plt.figure() # 新图 0
                #plt.show()
                plt.savefig("./full/path_"+str(index)+ "_" + info + "+.png")
                plt.cla()
                #plt.close(index) # 关闭图 0
                index += 1
                ##
            
            print "@@@: ", nodesGroup
            #print GM1.mapping
            #print GM2.mapping
            #print GM3.mapping
            #print GM4.mapping
            print "##"
        else:
            somelist = [x for x in somelist if not set(nodesGroup).issubset(x)]            
    #return suspicious


amount = len(File2Graph())
for s in range(amount):
    main(s, amount - 12)



"""
# *** 没有用的代码 *** #
'''
G=nx.DiGraph()
G.add_node(1, time='A')
G.add_node(2, time='B')
G.add_edge(1,2)
H=nx.DiGraph()
H.add_node(2, time='B')
H.add_node(1, time='A')
H.add_node(13, time='A')
H.add_edge(1,2)
H.add_edge(1,3)
H.nodes()
K = H.subgraph((1,2))
GM = nx.isomorphism.DiGraphMatcher(K, G)#, node_match=iso.categorical_node_match('time', None))
GM.is_isomorphic()
import networkx.algorithms.isomorphism as iso
GM = nx.isomorphism.DiGraphMatcher(H, G)#, node_match=iso.categorical_node_match('time', None))
GM.subgraph_is_isomorphic()
ret = GM.subgraph_isomorphisms_iter()
for i in ret:
    print i
for g in ret:
    nx.draw(g)
    plt.show()
'''


def main():
    gList = File2Graph()
    somelist = [x for x in powerset(gList[4].nodes()) if len(x) > 1]

    suspicious = list()
    
    while True:
        if [] == somelist:
            break
        nodesGroup = somelist.pop(0)
        print nodesGroup
        
        sg = gList[4].subgraph(nodesGroup)
        '''
        labels=dict((n,d['name']) for n,d in sg.nodes(data=True)) 
        nx.draw(sg, labels=labels,node_size=1000)
        plt.show()
        raw_input()
        '''
        
        GM1 = nx.isomorphism.DiGraphMatcher(gList[0], sg, node_match=iso.categorical_node_match('name', None))
        GM2 = nx.isomorphism.DiGraphMatcher(gList[1], sg, node_match=iso.categorical_node_match('name', None))
        GM3 = nx.isomorphism.DiGraphMatcher(gList[2], sg, node_match=iso.categorical_node_match('name', None))
        GM4 = nx.isomorphism.DiGraphMatcher(gList[3], sg, node_match=iso.categorical_node_match('name', None))
        if GM1.subgraph_is_isomorphic() and GM2.subgraph_is_isomorphic() and GM3.subgraph_is_isomorphic() and GM4.subgraph_is_isomorphic():
            '''
            for s in suspicious:
                GM = nx.isomorphism.DiGraphMatcher(sg, s)
                GM.is_isomorphic()
                apd = 0
                break
                '''
            suspicious.append(sg)
            print "@@@: ", nodesGroup
            print GM1.mapping
            print GM2.mapping
            print GM3.mapping
            print GM4.mapping
            print "##"
        else:
            somelist = [x for x in somelist if not set(nodesGroup).issubset(x)]            
    return suspicious

ret = main()
for sg in ret:
    labels=dict((n,d['name']) for n,d in sg.nodes(data=True)) 
    nx.draw(sg, labels=labels,node_size=1000)
    plt.show()
def main():
    gList = File2Graph()
    somelist = [x for x in powerset(gList[4].nodes()) if len(x) > 1]

    suspicious = list()
    
    while True:
        if [] == somelist:
            break
        nodesGroup = somelist.pop(0)
        print nodesGroup
        
        sg = gList[4].subgraph(nodesGroup)
        '''
        labels=dict((n,d['name']) for n,d in sg.nodes(data=True)) 
        nx.draw(sg, labels=labels,node_size=1000)
        plt.show()
        raw_input()
        '''
        
        GM1 = nx.isomorphism.DiGraphMatcher(gList[0], sg, node_match=iso.categorical_node_match('name', None))
        GM2 = nx.isomorphism.DiGraphMatcher(gList[1], sg, node_match=iso.categorical_node_match('name', None))
        GM3 = nx.isomorphism.DiGraphMatcher(gList[2], sg, node_match=iso.categorical_node_match('name', None))
        GM4 = nx.isomorphism.DiGraphMatcher(gList[3], sg, node_match=iso.categorical_node_match('name', None))
        if GM1.subgraph_is_isomorphic() and GM2.subgraph_is_isomorphic() and GM3.subgraph_is_isomorphic() and GM4.subgraph_is_isomorphic():
            '''
            for s in suspicious:
                GM = nx.isomorphism.DiGraphMatcher(sg, s)
                GM.is_isomorphic()
                apd = 0
                break
                '''
            suspicious.append(sg)
            print "@@@: ", nodesGroup
            print GM1.mapping
            print GM2.mapping
            print GM3.mapping
            print GM4.mapping
            print "##"
        else:
            somelist = [x for x in somelist if not set(nodesGroup).issubset(x)]            
    return suspicious

ret = main()
'''for sg in ret:
    labels=dict((n,d['name']) for n,d in sg.nodes(data=True)) 
    nx.draw(sg, labels=labels,node_size=1000)
    plt.show()
    '''

gList = File2Graph()


#index = 0
for sg in ret2:
    labels=dict((n,d['name']) for n,d in sg.nodes(data=True)) 
    nx.draw(sg, labels=labels,node_size=1000)
    plt.show()
    #plt.savefig("path_"+str(index)+".png")
    #index += 1

"""