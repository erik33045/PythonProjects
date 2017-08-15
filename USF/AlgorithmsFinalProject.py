import os
import networkx as nx
import datetime
import random


#Main function
def algorithms_final_project():

    start_time = datetime.datetime.now()
    input_file_name = "input.txt"
    input_file = open(input_file_name, 'r')

    # get number of nodes and edges
    line = input_file.readline().split()
    number_of_nodes, number_of_edges = int(line[0]), int(line[1])

    #Create the graph of nodes and edges
    g = generate_graph(input_file, number_of_edges, number_of_nodes)

    input_file.close()

    #Perform the linear maximization algorithm
    output_file = open("output-linear.txt", 'wb')
    linear_found_edges = linear_maximization(output_file, g, number_of_nodes)
    output_file.close()

    #Perform the random cut algorithm
    output_file = open("output-random.txt", 'wb')
    random_found_edges = random_cut(output_file, g, number_of_nodes, 10)
    output_file.close()

    elapsed_time = datetime.datetime.now() - start_time
    output_file = open("Hendrickson.txt", 'wb')
    output_file.write(str(total_time_in_milliseconds(elapsed_time)) + "\n")
    output_file.close()

    output_file = open("Hendrickson.txt", 'a')

    #Check which algorithm had the most number of found edges and copy that to the final output file
    if random_found_edges > linear_found_edges:
        input_file = open("output-random.txt", 'r')
    else:
        input_file = open("output-linear.txt", 'r')

    for line in input_file:
            output_file.write(line)

    input_file.close()
    output_file.close()

    #Remove temporary output files
    os.remove("output-random.txt")
    os.remove("output-linear.txt")


def generate_graph(input_file, number_of_edges, number_of_nodes):
    # parse input into graph
    g = nx.Graph()
    # add each node to graph
    # Time Complexity: O(m)*time_to_add_node
    for node in range(number_of_nodes):
        g.add_node(node + 1, group=1)

    # read in each line and add the corresponding edge to the graph, g
    # Time Complexity: O(m)*time_to_add_edge
    for edge in range(number_of_edges):
        line = input_file.readline().split()
        g.add_edge(int(line[0]), int(line[1]))
    return g


#Test function that generates a number of nodes and edges based on user inputs
def graph_generator(number_of_nodes, connectedness_of_graph, name_of_test_file):
    #How connected the graph is, percentage 0-100
    connectedness_ratio = float(connectedness_of_graph / float(100))
    #This is how we know how many edges to add to each node
    number_of_edges_per_node = int(number_of_nodes * connectedness_ratio)

    #this is the output file to write to
    output_file = open(name_of_test_file, 'wb')

    total_number_of_edges = 0

    #for loop to calculate the total number of edges
    for node in range(1, number_of_nodes+1):
        for edge in range(1, number_of_edges_per_node+1):
            if edge == node:
                continue
            total_number_of_edges += 1

    #Write the number of nodes and edges
    output_file.write(str(number_of_nodes) + " " + str(total_number_of_edges) + "\n")

    #write out each edge
    for node in range(1, number_of_nodes+1):
        for edge in range(1, number_of_edges_per_node+1):
            if edge == node:
                continue
            output_file.write(str(node) + " " + str(edge) + "\n")


#This function counts the total number of elapsed milliseconds and returns them
def total_time_in_milliseconds(elapsed_time):
    return (float(elapsed_time.seconds) * float(1000)) + (float(elapsed_time.microseconds) / float(1000))


#This Algorithm will go through each node and attempt to add it to group a, and check if going from B to A increases
#the number of crossing edges
def linear_maximization(output_file, g, number_of_nodes):

    #initialize current crossing edge count to 0
    max_count = 0

    # a list of the nodes to be shuffled

    nodes = []
    #list to contain 1 group of nodes
    first_group = []
    # a second list used to form a second_group
    second_group = []

    # place all the nodes into list to be shuffled and initialize the group 1 list to contain all nodes
    # Time Complexity: O(n)
    for i in range(1, number_of_nodes+1):
        nodes.append(i)
        first_group.append(i)

    random.shuffle(nodes)

    # for all nodes
    # Time Complexity: O(mn)
    for i in range(number_of_nodes):
        # get node to be examined
        current_node = nodes[i]

        # get set of neighbors
        # Time complexity: O(m)
        node_neighbors = g.neighbors(current_node)
        node_neighbors_set = set(node_neighbors)

        # determine amount of edges that are and are not currently crossing between groups
        current_non_cross_edges = len(node_neighbors_set.intersection(first_group))
        current_cross_edges = len(node_neighbors) - current_non_cross_edges

        # determine the net difference of crossing edges if the node is moved to group 2
        net_cross_edges_after_switch = current_non_cross_edges - current_cross_edges

        # if there will be a positive addition of edges after the switch then add them to the edge count
        if net_cross_edges_after_switch > 0:
            max_count += net_cross_edges_after_switch
            #append node from first group
            second_group.append(current_node)
            #remove node from first group
            first_group.remove(current_node)
        # if this new configuration isn't better than the best...

    output_file.write(str(max_count) + "\n")

    #write all entries in the first group seperated by spaces excluding the last entry
    [output_file.write(str(n) + " ") for n in first_group]
    #write the last entry with a new line
    output_file.write('\n')

    #write all entries in the second group seperated by spaces excluding the last entry
    [output_file.write(str(n) + " ") for n in second_group]
    #write the last entry with a new line
    output_file.write('\n')

    return max_count


def random_cut(output_file, g, number_of_nodes, seconds_to_run):
    """
    randomly splits graph nodes into 2 groups and reports the number of crossing edges between them
    """

    # mark start_time
    start_time = datetime.datetime.now()
    elapsed_time_seconds = 0

    final_cross_count = 0
    final_first_group = []
    final_second_group = []

    #initialize first group to contain all nodes
    for i in range(number_of_nodes):
        final_first_group.append(i+1)

    node_list = g.nodes()

    #keep searching for best solution until end of given runtime
    while elapsed_time_seconds < seconds_to_run:

        #set group attribute of random number of nodes to group 2
        num_choose = random.randint(0, number_of_nodes)
        for i in range(num_choose):
            change_node = random.randint(1, number_of_nodes)
            g.node[change_node]["group"] = 2

        #initialize group lists
        first_group = []
        second_group = []
        crossing_edges = 0

        #append nodes to appropriate lists
        for x in node_list:
            if g.node[x]["group"] == 1:
                first_group.append(x)
            else:
                second_group.append(x)

        #if a neighbor of a node in the first_group is not in group 1 as well it is a cross edge and we increment
        for x in first_group:
            for neighbor in g[x].keys():
                if g.node[neighbor]["group"] == 2:
                    crossing_edges += 1

        # we keep the groups if the cross edge total is improved
        if crossing_edges > final_cross_count:
            final_cross_count = crossing_edges
            final_first_group = first_group[:]
            final_second_group = second_group[:]

        #reset group settings
        for x in node_list:
            g.node[x]["group"] = 1

        elapsed_time_seconds = (datetime.datetime.now() - start_time).seconds

    output_file.write(str(final_cross_count) + '\n')

    #write all entries in the first group seperated by spaces excluding the last entry
    [output_file.write(str(n) + " ") for n in final_first_group]
    #write the last entry with a new line
    output_file.write('\n')

    #write all entries in the second group seperated by spaces excluding the last entry
    [output_file.write(str(n) + " ") for n in final_second_group]
    #write the last entry with a new line
    output_file.write('\n')

    return final_cross_count


def check_output(output_file, g, solution_filename):
    """ Function that checks if a given number of crossing edges is correct
     for an input graph and an output file"""
    node_list = g.nodes()

    #get output groups
    solution_file = open(solution_filename, 'r')

    #get reported edges
    reported_crossing_edges = int(solution_file.readline())

    # create node group lists
    group_1 = map(int, solution_file.readline().split())
    group_2 = map(int, solution_file.readline().split())

    #reset group attributes
    for node in node_list:
        g.node[node]["group"] = -1

    # set group attributes depending on the group
    for g1_vertex in group_1:
        g.node[g1_vertex]["group"] = 1

    for g2_vertex in group_2:
        g.node[g2_vertex]["group"] = 2

    # check to make sure all nodes are properly labeled
    for n in node_list:
        if g.node[n]["group"] == -1:
            output_file.write("All nodes not included in groups! Bad solution!\n")
            return

    crossing_edges = 0

    #count crossing edges
    for vertex in group_1:
        for neighbor in g[vertex].keys():
            if g.node[neighbor]["group"] == 2:
                crossing_edges += 1

    if crossing_edges == reported_crossing_edges:
        output_file.write("This is a correct solution. Hooray!")
    elif crossing_edges > reported_crossing_edges:
        output_file.write("Not all crossing edges reported. It should be " + str(crossing_edges) + "\n")
    else:
        output_file.write("More crossing edges reported than there exist. EPIC FAILURE\n")

    solution_file.close()
    return

#This is to be able to run the file through command line
if __name__ == "__main__":
    algorithms_final_project()
