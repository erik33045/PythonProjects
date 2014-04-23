import os
import networkx as nx
import datetime
import random
import shutil


#Main function
def algorithms_final_project():
    input_file_name = "input_20knodes_100kedges"

    #Perform the linear maximization algorithm
    input_file = open(input_file_name, 'r')
    output_file = open("output-linear.txt", 'wb')
    linear_found_edges = linear_maximization(input_file, output_file)
    input_file.close()
    output_file.close()

    #Perform the random cut algorithm
    input_file = open(input_file_name, 'r')
    output_file = open("output-random.txt", 'wb')
    random_found_edges = random_cut(input_file, output_file, 10)
    input_file.close()
    output_file.close()

    #Check which algorithm had the most number of found edges and copy that to the final output file
    if random_found_edges > linear_found_edges:
        shutil.copyfile("output-random.txt", "Hendrickson.txt")
    else:
        shutil.copyfile("output-linear.txt", "Hendrickson.txt")

    input_file = open(input_file_name, 'r')
    output_file = open("output-check.txt", 'wb')
    check_output(input_file, output_file, "output-linear.txt")
    input_file.close()
    output_file.close()


    #Remove temporary output files
    #os.remove("output-random.txt")
    #os.remove("output-linear.txt")




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
def linear_maximization(input_file, output_file):
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
        
    # add each node to ensure it's there
    for i in range(1, int(vals[0])+1):
        g.add_node(i)
        
    # place all the nodes and their neighbors into the neighbors list
    for i in range(1, len(g.nodes())+1):
        neighbors.append([i, g[i].keys()])

    # the number of nodes to check (default to all of them)
    # set to the total number of nodes
    node_num = int(vals[0])
    # randomize the order of the list
    random.shuffle(neighbors)

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
        if count >= max_count:
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

    return max_count


def random_cut(input_file, output_file, seconds_to_run):
    '''randomly splits graph nodes into 2 groups and reports the number of crossing edges between them '''

    # mark start_time
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
        g.add_node(node+1, group=1)

    for edge in range(number_of_edges):
        line = input_file.readline().split()
        g.add_edge(int(line[0]), int(line[1]))


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

    return final_cross_count

def check_output(input_file, output_file, solution_filename):

    g = nx.Graph()


    #create graph
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

    g.add_nodes_from(list(node_dictionary), group= -1)
    g.add_edges_from(edge_list)

    node_list = g.nodes()

    #get output groups

    solution_file = open(solution_filename, 'r')
    solution_file.readline() # eat time
    reported_crossing_edges = int(solution_file.readline()) #get reported edges

    group_1 = map(int, solution_file.readline().split())
    group_2 = map(int, solution_file.readline().split())

    for g1_vertex in group_1:
        g.node[g1_vertex]["group"] = 1

    for g2_vertex in group_2:
        g.node[g2_vertex]["group"] = 2

    for n in node_list:
        if g.node[n]["group"]==-1:
            output_file.write("All nodes not included in groups! Bad solution!\n")
            return

    crossing_edges = 0

    for vertex in group_1:
        for neighbor in g[vertex].keys():
            if g.node[neighbor]["group"] == 2:
                crossing_edges += 1

    if crossing_edges == reported_crossing_edges:
        output_file.write("This is a correct solution. Hooray!")
    elif crossing_edges > reported_crossing_edges:
        output_file.write("{}{}{}".format("Not all crossing edges reported. It should be ", crossing_edges, "\n"))
    else:
        output_file.write("More crossing edges reported than there exist. EPIC FAILURE\n")

    solution_file.close()
    return

#This is to be able to run the file through command line
if __name__ == "__main__":
    algorithms_final_project()
