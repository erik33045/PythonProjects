import networkx as nx
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


def adams_solution():
    input_file = open('input-10000nodes-fullyconnected.txt', 'r')

    g = nx.Graph()
    vals = input_file.readline().split()

    count = 0
    max_count = 0
    ordered = []
    check = []

    for i in range(1, int(vals[1])+1):
        edge = input_file.readline().split()
        edge = map(int, edge)
        u = edge[0]
        v = edge[1]
        g.add_edge(u, v)

    for i in range(1, len(g.nodes())+1):
        ordered.append([i, sorted(g[i].keys())])

    ordered.sort(key=lambda s: len(s[1]), reverse=True)

    node_num = len(g.nodes())

    for i in range(0, node_num):
        check.append(ordered[i][0])
        c = check[-1]
        length = len(g.neighbors(c)) - (len(set(g.neighbors(c)).intersection(check))) * 2
        count += length
        if count > max_count:
            max_count = count
        elif count < max_count:
            del check[-1]

    print '\n'
    print 'max crossing edges:', max_count
    input_file.close()


if __name__ == "__main__":
    algorithms_final_project()


