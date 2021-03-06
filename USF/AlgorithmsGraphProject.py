import networkx as nx
import matplotlib.pyplot as plt


class Node:
    x = 0
    y = 0
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
        self.x = float(index.split(',')[0])
        self.y = -float(index.split(',')[1])
        self.edges = []

    # So if the compare node is the opposite color or the end, add it as an edge to the current node
    def can_add_compare_node_as_edge(self, compare_node):
        return (self.color == "B" and (compare_node.color == "R" or compare_node.color == "Y")) or (
            self.color == "R" and (compare_node.color == "B" or compare_node.color == "Y"))

    # Traverse through the node dictionary in the direction of the node and add all possible edges
    def add_edges_to_node(self, node_dictionary, number_of_columns, number_of_rows):

        # If both directions are 0, we are at the end node, so return
        if self.direction_horizontal == 0 and self.direction_vertical == 0:
            return

        position = self.index.split(',')
        row_position = int(position[1]) + self.direction_vertical
        column_position = int(position[0]) + self.direction_horizontal

        # stay within the bounds of the array!
        while (0 <= row_position < number_of_rows) and (0 <= column_position < number_of_columns):
            # Change position based on the node's direction

            # Here is the node we are comparing against
            compare_node = node_dictionary["" + str(column_position) + "," + str(row_position)]

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
            index = "" + str(column) + "," + str(row)
            node_to_add = Node(index, node.split('-'))
            node_dictionary[index] = node_to_add
            column += 1
        row += 1

    return node_dictionary


def draw_graph(g, node_dictionary, file_name):
    custom_labels = {}
    custom_colors = {}
    pos = {}
    for index in node_dictionary.keys():
        node = node_dictionary[index]
        custom_labels[node.index] = node.direction

        # Custom label and color the start node
        if node.index == "0,0":
            custom_labels[node.index] = node.color + "-" + node.direction
            custom_colors[node.index] = "g"
        else:
            custom_colors[node.index] = node.color.lower()

        # Mark the position
        pos[node.index] = (node.x, node.y)

    nx.draw(g, node_list=custom_labels.keys(),
            labels=custom_labels,
            node_color=custom_colors.values(), pos=pos)

    plt.savefig(file_name, dpi=120)


def create_shortest_path_string(shortest_path):
    shortest_path_string = ""
    for index in range(0, len(shortest_path) - 1):
        if index + 1 > len(shortest_path) - 1:
            return
        else:
            step = shortest_path[index]
            next_step = shortest_path[index + 1]
            change_horizontal = int(next_step.split(',')[0]) - int(step.split(',')[0])
            change_vertical = int(next_step.split(',')[1]) - int(step.split(',')[1])

            direction_change = ""

            if change_vertical < 0:
                direction_change += "N"
            elif change_vertical > 0:
                direction_change += "S"
            if change_horizontal < 0:
                direction_change += "W"
            elif change_horizontal > 0:
                direction_change += "E"

            if direction_change == "N" or direction_change == "S":
                direction_change += "-" + str(abs(change_vertical))
            elif direction_change == "W" or direction_change == "E":
                direction_change += "-" + str(abs(change_horizontal))
            else:
                direction_change += "-" + str(abs(change_horizontal))

            shortest_path_string += direction_change + " "
    return shortest_path_string


def solve_maze(input_file, output_file, maze_number):
    number_of_rows = number_of_columns = int(input_file.readline())
    node_dictionary = create_node_dictionary(input_file, number_of_rows)
    max_index = "" + str(number_of_rows - 1) + "," + str(number_of_columns - 1)
    nodes = []
    edges = []
    for index in node_dictionary.keys():
        node = node_dictionary[index]
        nodes.append(node.index)
        node.add_edges_to_node(node_dictionary, number_of_columns, number_of_rows)
        for edge in node.edges:
            edges.append((index, edge))

    g = nx.DiGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)

    shortest_path = nx.algorithms.shortest_paths.generic.shortest_path(g, source="0,0", target=max_index)

    # write the output to the file
    output_file.write(create_shortest_path_string(shortest_path) + "\n" + "\n")

    # draw the graph and save it as a png
    draw_graph(g, node_dictionary, "Hendrickson_" + str(maze_number + 1) + ".png")

    # read blank line to get to correct place
    input_file.readline()


def main():
    input_file = open("input.txt", 'r')
    output_file = open("Hendrickson.txt", 'wb')

    number_of_mazes = int(input_file.readline())

    # read blank line to go to correct place in file
    input_file.readline()

    for maze in range(number_of_mazes):
        solve_maze(input_file, output_file, maze)

    input_file.close()
    output_file.close()


if __name__ == '__main__':
    main()
