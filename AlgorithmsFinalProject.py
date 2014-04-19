import networkx as nx
import datetime
import random


def algorithms_final_project():
    input_file_name = "input.txt"

    input_file = open(input_file_name, 'r')
    output_file = open("output-rank.txt", 'wb')
    rank_and_prune(input_file, output_file)
    input_file.close()
    output_file.close()

    input_file = open(input_file_name, 'r')
    output_file = open("output-random.txt", 'wb')
    random_cut(input_file, output_file, 20)
    input_file.close()
    output_file.close()


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


def total_time_in_milliseconds(elapsed_time):
    return (float(elapsed_time.seconds) * float(1000)) + (float(elapsed_time.microseconds) / float(1000))


def rank_and_prune(input_file, output_file):
    start_time = datetime.datetime.now()
    # create the graph for edge/node storage
    g = nx.Graph()
    # grab the first two values nodes/edges
    vals = input_file.readline().split()

    # check the count of the current grouping and set the cap for the max count encountered
    count = max_count = 0
    # a list of the nodes with their number of neighbors
    neighbors = []
    first_group = []
    # a second list used to form a second_group
    second_group = []

    # read in each line and add the corresponding edge to the graph, g
    for i in range(1, int(vals[1])+1):
        edge = input_file.readline().split()
        edge = map(int, edge)
        u = edge[0]
        v = edge[1]
        g.add_edge(u, v)

    # place all the nodes and their neighbors into the neighbors list
    for i in range(1, len(g.nodes())+1):
        neighbors.append([i, g[i].keys()])

    # the number of nodes to check (default to all of them)
    node_num = len(g.nodes())

    # check nodes until you reach the cap of num_nodes
    for i in range(0, node_num):
        # place the next node into the second group
        second_group.append(neighbors[i][0])
        # create a reference to the last node put into the second group
        last_node = second_group[-1]
        # set crossing_edges to the number of neighbors the most recently added node has
        # and remove any connections to nodes already in the group
        crossing_edges = len(g.neighbors(last_node)) - (len(set(g.neighbors(last_node)).intersection(second_group))) * 2
        # append these crossing_edges to the count of crossing edges
        count += crossing_edges
        # if the current configuration is better than the previous best...
        if count > max_count:
            # set this new max value
            max_count = count
        # if this new configuration isn't better than the best...
        elif count < max_count:
            # remove the most recently added node and keep going
            del second_group[-1]
            #append to first_group
            first_group.append(neighbors[i][0])

    elapsed_time = datetime.datetime.now() - start_time

    output_file.write(str(total_time_in_milliseconds(elapsed_time)) + "\n")
    output_file.write(str(max_count) + "\n")

    #write all entries in the first group seperated by spaces excluding the last entry
    [output_file.write(str(n) + " ") for n in first_group[0:-1]]
    #write the last entry with a new line
    output_file.write(str(first_group[-1]) + '\n')

    #write all entries in the second group seperated by spaces excluding the last entry
    [output_file.write(str(n) + " ") for n in second_group[0:-1]]
    #write the last entry with a new line
    output_file.write(str(second_group[-1]) + '\n')

def random_cut(input_file, output_file, seconds_to_run):

    start_time = datetime.datetime.now()
    elapsed_time_seconds = 0

    g = nx.Graph()

    line = input_file.readline().split()
    number_of_nodes, number_of_edges = int(line[0]), int(line[1])

    node_dictionary = {}
    edge_list = []

    final_cross_count = 0
    final_first_group = []
    final_second_group = []

    for node in range(number_of_nodes):
        node_dictionary[node+1] = str(node+1)

    for edge in range(number_of_edges):
        line = input_file.readline().split()
        edge_tuple = (int(line[0]), int(line[1]))
        edge_list.append(edge_tuple)

    g.add_nodes_from(list(node_dictionary), group=1)
    g.add_edges_from(edge_list)

    node_list = g.nodes()

    while elapsed_time_seconds < seconds_to_run:
        #set group attribute of random number of nodes to group 2
        num_choose = random.randint(0, number_of_nodes)
        for i in range(num_choose):
            change_node = random.randint(1, number_of_nodes)
            g.node[change_node]["group"] = 2

        first_group = []
        second_group = []
        crossing_edges = 0

        for x in node_list:
            if g.node[x]["group"] == 1:
                first_group.append(x)
            else:
                second_group.append(x)

        for x in first_group:
            for neighbor in g[x].keys():
                if g.node[neighbor]["group"] == 2:
                    crossing_edges += 1

        if crossing_edges > final_cross_count:
            final_cross_count = crossing_edges
            final_first_group = first_group[:]
            final_second_group = second_group[:]

        #reset group settings
        for x in node_list:
            g.node[x]["group"] = 1

        elapsed_time_seconds = (datetime.datetime.now() - start_time).seconds

    elapsed_time = datetime.datetime.now() - start_time

    output_file.write(str(total_time_in_milliseconds(elapsed_time)) + '\n')
    output_file.write(str(final_cross_count) + '\n')

    #write all entries in the first group seperated by spaces excluding the last entry
    [output_file.write(str(n) + " ") for n in final_first_group[0:-1]]
    #write the last entry with a new line
    output_file.write(str(final_first_group[-1]) + '\n')

    #write all entries in the second group seperated by spaces excluding the last entry
    [output_file.write(str(n) + " ") for n in final_second_group[0:-1]]
    #write the last entry with a new line
    output_file.write(str(final_second_group[-1]) + '\n')


if __name__ == "__main__":
    algorithms_final_project()