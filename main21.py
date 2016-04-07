#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, copy, csv
import networkx as nx
import matplotlib.pyplot as plt
import networkx.algorithms.isomorphism as iso
from itertools import chain, combinations


'''
	将属性划分为权重的关系
	高两位为属性关系，讲四种属性关系值赋为权重值
	若高于两位，则最后一位为符号位，即：
	1 ，表负关系（负相接，负相切）
	0 ， 表正关系（正相接， 正相切）
	符号位和高两位之间若存在位数，则将其附属在后缀中，即权重值中给小数点后第一位：
	0， 值为 0.0
	1， 值为0.1

FH = {'1': '-', '0': '+'}

HZ = {'0': '0', '1': '1'}

def getWeight(weightstr):
	length = len(weightstr)
	sx = SX.get(weightstr[:2], '-1')
	fh = '+' if length < 3 else FH.get(weightstr[-1])
	hz = '0'
	if length > 3:
		hz += '.'
		for x in xrange(3, length):
			hz += HZ.get(weightstr[2])

	#print sx, hz, fh, type(sx), type(hz), type(fh)
	weight = eval(fh + '(' + str(sx) + '+'+ str(hz) + ')' )
	return weight

'''
SX = {
	'00': '1', 
	'01': '2', 
	'10': '3', 
	'11': '4', 
}
def getWeight2(weightstr):
	sx = SX.get(weightstr[:2], '-1')
	weight = sx + weightstr[2+1:] if len(weightstr) > 2 else sx
	return weight


def cache2Graph(c):
	nodes = c.get('nodes', [])
	edges = c.get('edges', [])
	if not nodes or not edges:
		return None

	graph = nx.DiGraph()
	for node in nodes:
		graph.add_node(node, name=node)
	for edge in edges:
		n1 = edge[0]
		n2 = edge[1]
		w = getWeight2(edge[-1])
		#print w, 
		graph.add_edge(n1, n2, weight=w)
	#print 
	return graph
	
def getNodes(nodestr):
	#print '=====NODE STR : %s', nodestr
	idx = nodestr.index(':') if ':' in nodestr else nodestr.index(u'：'.encode('utf-8'))
	return nodestr[idx+1: ].strip().split()
def loadCSVFile(filepath):
	edges = []
	cache = dict()
	with open(filepath) as f:
		reader = csv.reader(f)
		for line in reader:
			if line and line[0].startswith('label'):
				#print line
				nodes = getNodes(line[0])
				cache['nodes'] = nodes
			elif line and len(line) == 3:
				edges.append(line)
				
		cache['edges'] = edges
	return cache

def getAllCSVFilesPath(path):
	#print 'GET ALL PATH!!!'
	files = os.listdir(path)
	return [path+'/'+f for f in files if f.endswith('.csv')]
 
def getAllGraphs(path):
	#print '---------now path %s' % path
	#print 'START GET ALL GRAPHS'
	gList = []
	
	filepaths = getAllCSVFilesPath(path)
	for p in filepaths:
		#print p
		cache = loadCSVFile(p)
		graph = cache2Graph(cache)
		gList.append(graph)
	#print '----- GRAPHS END -----'
	return gList

def drawPic(g, picname):
	labels = dict((n, d.get('name')) for n,d in g.nodes(data=True))
	elarge = [(u, v) for (u, v, d) in g.edges(data=True) if d.get('weight') > 0]
	esmall = [(u, v) for (u, v, d) in g.edges(data=True) if d.get('weight') < 0]
	ezero = [(u, v) for (u, v, d) in g.edges(data=True) if d.get('weight') == 0]
	edgeLabels = dict(((u, v),d.get('weight')) for (u, v, d) in g.edges(data=True))
	pos = nx.spring_layout(g)
	nx.draw_networkx_nodes(g, pos, node_size=700)
	nx.draw_networkx_labels(g, pos)
	nx.draw_networkx_edges(g, pos, edgelist=ezero, edge_color='b', width=2)
	nx.draw_networkx_edges(g, pos, edgelist=elarge)
	nx.draw_networkx_edges(g, pos, edgelist=esmall, style='dashed', edge_color='r')
	#print edgeLabels
	
	nx.draw_networkx_edge_labels(g, pos,edge_labels=edgeLabels, font_color='b')
	plt.savefig(picname)
	plt.cla()
	
def powerset(iterable, r):
	'''
	产生一个数组所有的组合可能
	powerset([1,2,3]) -> [() (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)]
	'''
	s = list(iterable)
	return combinations(s, r)
			
			
	
		


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
	#print '*** start ***'
	v = 0
	sptList = []
	for i in range(len(gList)):
		g = gList[i]
		GM = nx.isomorphism.DiGraphMatcher(g, sg)
		if GM.subgraph_is_isomorphic():
			v += 1
			sptList.append(i)
	#print '*** end.. ***'
	return v, sptList

index = 0
'''
	index 生成文件名计数 int
	seed_number 作为图拆解种子的序号 int
	minspt 最小支持数 int
'''
	

def main(seed_number, minspt, gList):
	global index
	global suspicious
	dellist = []
	#print seed_number
	
	g_seed = gList[seed_number]
	#print gList
	#print 'G_SEED---------', type(g_seed), g_seed == gList[seed_number]

	xCount = 0
	for x in xrange(len(g_seed.nodes())):
		print '#### ROUND ', xCount
		#print '###   GET POWER SET ###'
		somelist = [i for i in powerset(g_seed.nodes(), x) if len(i) > 1]
		for g in dellist:
			print 'g .... is ', g
			somelist = [i for i in somelist if not set(g).issubset(i)]

		#print ' ###  END POWER SET ###'
		#print len(somelist)
		tmp = 0
		while somelist:
			nodesGroup = somelist.pop(0)

			print "$$ total: ", len(somelist), nodesGroup
			sg = g_seed.subgraph(nodesGroup)
			spt, sptList = supportValue(gList, sg)
			if spt >= minspt:
				print 'if ......'
				info = '-'.join(str(i) for i in sptList)
	
				if not isomorphism_set(sg):
					suspicious.append(sg)
					##
					#labels=dict((n,d['name']) for n,d in sg.nodes(data=True)) 
					picname = "./full2/path_"+str(xCount)+'_'+str(tmp)+'_'+str(seed_number)+'_'+str(index)+ "_" + info + "+.png"
					#print picname
					drawPic(sg, picname)
					##
				print "@@@: ", nodesGroup
				#print GM1.mapping
				#print GM2.mapping
				#print GM3.mapping
				#print GM4.mapping
				print "##"
			else:
				print 'else .....'
				dellist.append(nodesGroup)
				somelist = [x for x in somelist if not set(nodesGroup).issubset(x)]			   
				print 'end....else'
				#print 'somelist-----------', somelist
			tmp += 1
		xCount += 1
if __name__ == '__main__':

	'''
	somelist = [x for x in powerset(range(20)) if len(x) > 1]
	print somelist
	'''
	
	path = '../12,27'
	gList = getAllGraphs(path)
	amount = len(gList)
	minsup = 0.7 * amount * 10 / 10 + 1
	#print '--amount is %s' % amount
	#print '--amount/2 + 1=', amount/2 + 1
	for s in xrange(amount):
		main(s, minsup, gList)




	'''
	f = loadCSVFile('../12,27/MG41.csv')
	g = cache2Graph(f)


	for w in ('000', '01', '10', '101', '0010', '0011', '0000', '1101'):
		wght = getWeight(w)
		print 'the code is %s, and the weight is %s' %(w, wght)
	'''
		

	
	
	
