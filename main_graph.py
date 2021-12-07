import networkx as nx
import matplotlib.pyplot as plt
import pprint

import device_info as di
import center_alg as ca
import spath as sp
import getdata as data
import setdata
import sys
import threading

def methode(vlan):
	print("STARTING METHODE FOR VLAN {0}".format(vlan))

	G = nx.Graph()
	print(G)

	print("--------------- ADD NODES ----------------")
	node_list=data.getNodesList()
	print(node_list)

	G.add_nodes_from(node_list)

	print("--------------- ADD EDGES ----------------")
	edge_list=data.getEdgesList()

	G.add_edges_from(edge_list)

	print("--------------- GRAPH BUILT ----------------")
	print(G)

	print()


	options={
		#'node_color': 'cyan',
		'node_size': 900,
		'width': 1,
		'node_shape': 's',			#https://matplotlib.org/stable/api/markers_api.html
	}

	pos={1:(0.5,1),2:(0.25,0.5),3:(0.75,0.5),4:(0,0),5:(1,0),}
	lab={1:" SW1",2:" SW2",3:" SW3",4:" SW4",5:" SW5"}



	#access_switches = data.getAccessSwitchList(vlan)
	access_switches = [1,3,5]
	print("------------Shortest Path-------------")

	print("Acces port switch devices: "+str(access_switches))
	sp.weightCreator(G,access_switches)
	print("Weights after modification:")
	# print(G.edges.data("weight"))
	print(G.edges.data())
	substracted_edges = [item for item in G.edges if item not in nx.maximum_spanning_tree(G).edges]
	print(substracted_edges)

	print("----------CENTER----------")
	center = ca.centerAlg(nx.maximum_spanning_tree(G),G)
	print("-------------------------")

	print("----------CHANGE ROOT PRIO----------")
	setdata.Threaded(setdata.change_root,vlan)
	setdata.change_root(di.getDevices()[center-1],str(4096),vlan)
	print("------------------------------------")

	print("----------CHANGE PORT COSTS----------")
	substracted_edges = [item for item in G.edges if item not in nx.maximum_spanning_tree(G).edges]
	print(substracted_edges)
	setdata.ThreadCost(setdata.change_port_cost,substracted_edges,G,100,vlan)

	tree_edges = list(nx.maximum_spanning_tree(G).edges)
	print(tree_edges)
	setdata.ThreadCost(setdata.change_port_cost,tree_edges,G,4,vlan)
	print("------------------------------------")

	#Color map: Red = Root bridge, Green = Access port switch, Cyan = Other
	color_map = ["red" if node == center else "#50C878" if node in access_switches else "cyan" for node in G]


	subax1 = plt.subplot(121)  			#Ez egy grid_layout, ami 1x2-es és az első grdibe megy
	nx.draw(G, pos=pos, labels=lab, with_labels=True,node_color = color_map, **options)#,pos=nx.random_layout(G))
	plt.title("Topology")

	subax1 = plt.subplot(122)			#második grid.
	nx.draw(nx.maximum_spanning_tree(G), pos = pos, labels=lab, with_labels=True,node_color = color_map, **options)
	plt.title("Maximum Spanning Tree")


	fig = plt.gcf()
	fig.set_size_inches(8.5, 5.5)
	fig.suptitle("VLAN "+str(vlan),fontsize = 16)
	fig.canvas.manager.set_window_title("VLAN "+str(vlan))
	plt.show()


def Threaded(function,vlans):
    
	threads = len(vlans)

	jobs = []
	for i in range(0,threads):
		thread = threading.Thread(target=function, args=(vlans[i],))
		jobs.append(thread)
		thread.start()

	for k in jobs:
		k.join()

vlans = [100,200,300]
methode(vlans[0])
#methode(vlans[1])
#methode(vlans[2])