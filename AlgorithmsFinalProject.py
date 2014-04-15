import networkx as nx
import matplotlib.pyplot as plt


#randomization is a good factor to emply
#Loop and do the problems multiple times, then select the best possible solution
def algorithms_final_project():
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


if __name__ == "__main__":
    algorithms_final_project()
