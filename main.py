#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import copy
import networkx as nx
import matplotlib.pyplot as plt
import networkx.algorithms.isomorphism as iso
from itertools import chain, combinations


def powerset(iterable):
    '''
    产生一个数组所有的组合可能
    powerset([1,2,3]) -> [() (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)]
    '''
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def Cache2Graph(c):
    '''
    操作gList中每一个Cache，按行解析成Graph

    String -> Graph
    '''
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
    '''
    分割文件，缓存在gList中
    
    File -> gList [Str, ]
    '''
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

'''
def gList2gDict(gList):
    r = dict()
    for i, o in zip(range(len(gList)), gList):
        r[i] = dict()
        r[i]['origin'] = o
    return r
'''

suspicious = list()
def isomorphism_set(sg):
    '''
    维护全局的不同构图集合，用于去重复

    sg 新增图 Graph
    suspicious 集合，全局变量 [Graph, ]
    '''
    for s in suspicious:
        GM = nx.isomorphism.DiGraphMatcher(sg, s)
        if GM.is_isomorphic():
            return True
    return False

def supportValue(gList, sg):
    '''
    求支持数量，即gList中包含sg的图的数量

    gList [Graph, ]
    sg Graph
    '''
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

index = 0
def main(seed_number, minspt):
    '''
    index 生成文件名计数 int
    seed_number 作为图拆解种子的序号 int
    minspt 最小支持数 int
    '''
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

if __name__ == '__main__':
    amount = len(File2Graph())
    for s in range(amount):
        main(s, amount - 12)




