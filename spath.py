import networkx as nx

def weightCreator(G, accessTypeSwitches):
	n = len(accessTypeSwitches)
	sumpath = int((n*(n-1))/2)
	w = []
	for i in range(0,n):
		for j in range(i+1,n):
			sp = nx.shortest_path(G,accessTypeSwitches[i],accessTypeSwitches[j])
			print("Shortest path between: "+str(accessTypeSwitches[i])+
			" and "+str(accessTypeSwitches[j])+" :"+str(sp))
			w.append(sp)
	print("W: "+str(w))
	for paths in w:
		if(len(paths)!=0):
			for n in range(0,len(paths)-1):
				'''print(paths[n])
				print(paths[n+1])
				print()'''
				actual_weight = G[paths[n]][paths[n+1]]['weight']
				node_degrees = G.degree[paths[n]] + G.degree[paths[n+1]]
				listofNeighbours = G.neighbors(paths[0])
				adj_adder = 0
				if paths[len(paths)-1] in listofNeighbours:
					adj_adder = 10
				G[paths[n]][paths[n+1]]['weight'] = actual_weight + node_degrees + adj_adder
				'''print(paths[n])
				print(paths[n+1])
				print(G[paths[n]][paths[n+1]])
				print(G[1][2])
				print(G[2][1])'''

				