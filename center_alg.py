import networkx as nx

def centerAlg(G,originalG):
	longest = 0
	#path = []
	n = len(list(G.nodes))
	sumpath = int((n*(n-1))/2)

	ultramax_path = []
	calculated_max_path = []
	for i in range(1,n):
		actual_path_list = []
		for j in range(i+1,n+1):
			path = list(nx.all_simple_paths(G,source=i, target = j))
			#print(path)
			if len(path) != 0:
				actual_path_list.append(path[0])
		#print(actual_path_list)
		maxpath = max(actual_path_list,key=len)
		#print(str(i) + " + " + str(j) + ":")
		#print(maxpath)

		ultramax_path.append(maxpath)
		

	calculated_max_path = max(ultramax_path,key=len)
	print("Max path: -------> "+str(calculated_max_path))

	deleted_max_path = deleteNoneMaxDegree(calculated_max_path,G,originalG)
	print("Removed path: -------> "+str(deleted_max_path))


	middle = len(deleted_max_path)/2
	#print("middle point: "+str(middle))
	decided_middle = chooseMiddlePoint(middle,deleted_max_path,G)
	#print("decided middle point: "+str(decided_middle))
	the_chosen_middle_point = deleted_max_path[decided_middle]
	print("Center of the tree: "+str(the_chosen_middle_point))
	return the_chosen_middle_point

def chooseMiddlePoint(mp, path, G):
	middlePoint = 0
	if mp.is_integer() == True:
		if G.degree[path[int(mp)-1]] >= G.degree[path[int(mp)]]:
			middlePoint = int(mp)-1
		else:
			middlePoint = int(mp)
		return middlePoint
	else:
		return int(mp)

def deleteNoneMaxDegree(pathlist,G,originalG):
	del_list = []
	for l in pathlist:
		if G.degree[l] == originalG.degree[l]:
			del_list.append(l)
	return del_list
