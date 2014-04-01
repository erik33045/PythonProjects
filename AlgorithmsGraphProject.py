import networkx as nx
import matplotlib.pyplot as plt


class Node:
    index = ""
    color = ""
    direction = "0"
    direction_horizontal = 0
    direction_vertical = 0
    edges = []

    def __init__(self, index, attributes):
        if len(attributes) > 1:
            self.color = attributes[1]
            self.direction = attributes[0]
            if self.direction.find("W") > -1:
                self.direction_horizontal -= 1
            if self.direction.find("E") > -1:
                self.direction_horizontal += 1
            if self.direction.find("N") > -1:
                self.direction_vertical -= 1
            if self.direction.find("S") > -1:
                self.direction_vertical += 1
        else:
            self.color = "Y"

        self.index = index
        self.edges = []

    # So if the compare node is the opposite color or the end, add it as an edge to the current node
    def can_add_compare_node_as_edge(self, compare_node):
        return (self.color == "B" and (compare_node.color == "R" or compare_node.direction == "0")) or (
            self.color == "R" and (compare_node.color == "B" or compare_node.direction == "0"))

    # Traverse through the node dictionary in the direction of the node and add all possible edges
    def add_edges_to_node(self, node_dictionary, number_of_columns, number_of_rows):

        # If both directions are 0, we are at the end node, so return
        if self.direction_horizontal == 0 and self.direction_vertical == 0:
            return

        position = self.index.split(',')
        row_position = int(position[0]) + self.direction_vertical
        column_position = int(position[1]) + self.direction_horizontal

        # stay within the bounds of the array!
        while (0 <= row_position < number_of_rows) and (0 <= column_position < number_of_columns):
            # Change position based on the node's direction

            # Here is the node we are comparing against
            compare_node = node_dictionary["" + str(row_position) + "," + str(column_position)]

            if self.can_add_compare_node_as_edge(compare_node):
                self.edges.append(compare_node.index)

            row_position += self.direction_vertical
            column_position += self.direction_horizontal


def create_node_dictionary(input_file, number_of_rows):
    node_dictionary = {}
    row = 0
    for line in range(number_of_rows):
        column = 0
        nodes = input_file.readline().split()
        for node in nodes:
            index = "" + str(row) + "," + str(column)
            node_to_add = Node(index, node.split('-'))
            node_dictionary[index] = node_to_add
            column += 1
        row += 1

    return node_dictionary


def solve_maze():
    input_file = open("input.txt", 'r')
    output_file = open("Hendrickson.txt", 'wb')

    number_of_rows = number_of_columns = int(input_file.readline())
    node_dictionary = create_node_dictionary(input_file, number_of_rows)
    max_index = "" + str(number_of_rows-1) + "," + str(number_of_columns-1)

    nodes = []
    edges = []
    for index in node_dictionary.keys():
        node = node_dictionary[index]
        nodes.append(node.index)
        node.add_edges_to_node(node_dictionary, number_of_columns, number_of_rows)
        for edge in node.edges:
            edges.append((index, edge))

    custom_labels = {}
    custom_colors = {}
    for index in node_dictionary.keys():
        node = node_dictionary[index]
        custom_labels[node.index] = node.direction
        custom_colors[node.index] = node.color.lower()

    g = nx.DiGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)

    shortest_path = nx.algorithms.shortest_paths.generic.shortest_path(g, source="0,0", target=max_index, weight=None)
    nx.draw_graphviz(g, node_list=custom_labels.keys(),
                     labels=custom_labels,
                     node_color=custom_colors.values())
    plt.savefig("atlas.png", dpi=100)
    input_file.close()
    output_file.close()


if __name__ == '__main__':
    solve_maze()
