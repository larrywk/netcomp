#Python 3.7 Larry Weeks
# Recursive routine to find the highest MTBF path
import loadnodes3   
import pathcost3


def find_shortest_path(graph, start, end, path=[]):
        nodelist=loadnodes3.loadnodes({})
       
        path = path + [start]  # add current node to the end of the path
        if start == end:       # if path has reached destination
            return path        # return it as the answer
        if not start in graph:  # if there is no such node
            return None
        shortest = None
        for node in graph[start]:  # for each link from where we are
            if node not in path:    # and we haven't been there already
                newpath = find_shortest_path(graph, node, end, path)
                newcost=pathcost3.pathcost(newpath,nodelist)
                shortcost=0
                if shortest:
                    shortcost=pathcost3.pathcost(shortest,nodelist)
                if newpath:
                    #if not shortest or len(newpath) < len(shortest):
                   if not shortest or newcost > shortcost:
                        shortest = newpath
      
        return shortest

