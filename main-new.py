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
	00 : 1
	01 : 2
	10 : 3
	11 : 4
	与其后所有位数拼接赋为权重值，如：
	000 ： 10
	1011： 311
'''
SX = {
	'00': '1', 
	'01': '2', 
	'10': '3', 
	'11': '4', 
}

'''
	将属性编码转为权重值
'''
def getWeight(weightstr):
	sx = SX.get(weightstr[:2], '-1')
	weight = sx + weightstr[2+1:] if len(weightstr) > 2 else sx
	return weight

'''
	cache转换成带权有向图结构
	每个CSV对应一张图数据存储在一个cache中，
	cache： dictionary
	{
		'nodes': [n1, n2, ...]
		'edges': [[n1, n2, weight], ...]	
	}

'''
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
		w = getWeight(edge[-1])
		#print w, 
		graph.add_edge(n1, n2, weight=w)
	#print 
	return graph
	
'''
	获取CSV文件中存储的所有节点，所有节点在每行一 ‘label：’开头，且是一行字符串
	params:	
		nodesstr : str 节点字符串 
	return:
		list 节点列表
'''
def getNodes(nodestr):
	print '=====NODE STR : %s', nodestr
	idx = nodestr.index(':') if ':' in nodestr else nodestr.index(u'：'.encode('utf-8'))
	return nodestr[idx+1: ].strip().split()

'''
	读取CSV文件
	将每个csv文件存储在一个cache中，
	cache： dict
	{
		'nodes': [n1, n2, ...]
		'edges': [[n1, n2, weight], ...]	
	}
'''
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
'''
	获取该路径下的所有CSV文件的fullpath
	一个csv存储一副图片，多张图片用多个csv存在一个文件夹下
	param：
		path： str csv文件夹路径
	return:
		list: 所有csv的fullpath
	
'''
def getAllCSVFilesPath(path):
	print 'GET ALL PATH!!!'
	files = os.listdir(path)
	return [path+'/'+f for f in files if f.endswith('.csv')]
 
'''
	获取所有的Graph
	去给定文件夹路径下将所有csv文件转换为graph
	param：
		path： str csv文件夹路径
	return：
		gList： [graph1, graph2, ...]
'''
def getAllGraphs(path):
	#print '---------now path %s' % path
	print 'START GET ALL GRAPHS'
	gList = []
	
	filepaths = getAllCSVFilesPath(path)
	for p in filepaths:
		print p
		cache = loadCSVFile(p)
		graph = cache2Graph(cache)
		gList.append(graph)
	print '----- GRAPHS END -----'
	return gList

'''
	画图，
	带权图，将权值标出
'''
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
	
##############################################以下是你原来的代码

def powerset(iterable):
	'''
	产生一个数组所有的组合可能
	powerset([1,2,3]) -> [() (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)]
	'''
	s = list(iterable)
	for x in chain.from_iterable(combinations(s, r) for r in xrange(len(s)+1)):
		filename = 'temp' + str(len(x)) + '.csv'
		with open(filename, 'a+') as f:
			writer = csv.writer(f)
			writer.writerow(x)
			
			
	
		


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
'''
	index 生成文件名计数 int
	seed_number 作为图拆解种子的序号 int
	minspt 最小支持数 int
'''
	
def main(seed_number, minspt, gList):
	global index
	global suspicious
	
	g_seed = gList[seed_number]
	print '###   GET POWER SET ###'
	powerset(g_seed.nodes())

	somelist = [x for x in powerset(g_seed.nodes()) if len(x) > 1]
	print ' ###  END POWER SET ###'
	print somelist
	while True:
		if [] == somelist:
			break
		nodesGroup = somelist.pop(0)
		print "$$ total: ", len(somelist), nodesGroup
		sg = g_seed.subgraph(nodesGroup)
		spt, sptList = supportValue(gList, sg)
		if spt >= minspt:
			info = '-'.join(str(i) for i in sptList)
		
			if not isomorphism_set(sg):
				suspicious.append(sg)
				##
				labels=dict((n,d['name']) for n,d in sg.nodes(data=True)) 
				picname = "./full/path_"+str(index)+ "_" + info + "+.png"
				##
			print "@@@: ", nodesGroup
			#print GM1.mapping
			#print GM2.mapping
			#print GM3.mapping
			#print GM4.mapping
			print "##"
		else:
			somelist = [x for x in somelist if not set(nodesGroup).issubset(x)]			   

if __name__ == '__main__':

	'''
	somelist = [x for x in powerset(range(20)) if len(x) > 1]
	print somelist
	'''
	
	path = '../12,27'
	gList = getAllGraphs(path)
	amount = len(gList)
	print '--amount is %s' % amount
	print '--amount/2 + 1=', amount/2 + 1
	#for s in range(amount):
	
	#print 'now ----', s
	main(0, amount/2 + 1, gList)




	'''
	f = loadCSVFile('../12,27/MG41.csv')
	g = cache2Graph(f)


	for w in ('000', '01', '10', '101', '0010', '0011', '0000', '1101'):
		wght = getWeight(w)
		print 'the code is %s, and the weight is %s' %(w, wght)
	'''
		

	
	
	
