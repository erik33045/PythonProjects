import networkx as nx
import random
#import matplotlib.pyplot as plt


#randomization is a good factor to emply
#Loop and do the problems multiple times, then select the best possible solution
def algorithms_final_project():
    import matplotlib.pyplot as plt
    #Open the files
    input_file = open("input.txt", 'r')
    output_file = open("Hendrickson.txt", 'wb')

    #Read the number of expected datasets and place the file header in the correct place
    line = input_file.readline().split()
    number_of_nodes, number_of_edges = int(line[0]), int(line[1])

    node_dictionary = {}
    edge_list = []

    for node in range(number_of_nodes):
        node_dictionary[node+1] = str(node+1)

    for edge in range(number_of_edges):
        line = input_file.readline().split()
        edge_tuple = (int(line[0]), int(line[1]))
        edge_list.append(edge_tuple)

    g = nx.Graph()
    g.add_nodes_from(list(node_dictionary))
    g.add_edges_from(edge_list)
    nx.draw(g)
    plt.savefig("output", dpi=90)


def graph_generator(number_of_nodes, connectedness_of_graph, name_of_test_file):
    connectedness_ratio = float(connectedness_of_graph / float(100))
    number_of_edges_per_node = int(number_of_nodes * connectedness_ratio)

    output_file = open(name_of_test_file, 'wb')

    total_number_of_edges = 0
    for node in range(1, number_of_nodes+1):
        for edge in range(1, number_of_edges_per_node+1):
            if edge == node:
                continue
            total_number_of_edges += 1

    output_file.write(str(number_of_nodes) + " " + str(total_number_of_edges) + "\n")

    for node in range(1, number_of_nodes+1):
        for edge in range(1, number_of_edges_per_node+1):
            if edge == node:
                continue
            output_file.write(str(node) + " " + str(edge) + "\n")

def adams_solution(input_file):
  g = nx.Graph() # create the graph for edge/node storage

  vals = input_file.readline().split() # grab the first two values nodes/edges

  count = 0 # check the count of the current grouping
  max_count = 0 # set the cap for the max count encountered
  neighbors = [] # a list of the nodes with their number of neighbors
  second_group = [] # a second list used to form a second_group

  # read in each line and add the corresponding edge to the graph, g
  for i in range(1, int(vals[1])+1):
    edge = input_file.readline().split()
    edge = map(int, edge)
    u = edge[0]
    v = edge[1]
    g.add_edge(u, v)

  # place all the nodes and their neighbors into the neighbors list
  for i in range(1, len(g.nodes())+1):
    neighbors.append([i,g[i].keys()])

  # the number of nodes to check (default to all of them)
  node_num = len(g.nodes())

  # check nodes until you reach the cap of num_nodes
  for i in range(0, node_num):
    second_group.append(neighbors[i][0]) # place the next node into the second group
    last_node = second_group[-1] # create a reference to the last node put into the second group
    # set crossing_edges to the number of neighbors the most recently added node has
    # and remove any connections to nodes already in the group
    crossing_edges = len(g.neighbors(last_node)) - (len(set(g.neighbors(last_node)).intersection(second_group))) * 2
    count += crossing_edges # append these crossing_edges to the count of crossing edges
    if count > max_count: # if the current configuration is better than the previous best...
      max_count = count # set this new max value
    elif count < max_count: # if this new configuration isn't better than the best...
      del second_group[-1] # remove the most recently added node and keep going

  print 'max crossing edges:', max_count

  input_file.close() # close the file

if __name__ == "__main__":
    algorithms_final_project()


