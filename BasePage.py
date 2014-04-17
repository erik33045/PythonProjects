# noinspection PyUnresolvedReferences
import datetime
import AlgorithmsFinalProject


if '__main__' == __name__:
    number_of_nodes = 100
    connectedness_of_graph = 1
    name_of_test_file = "input-test.txt"

    AlgorithmsFinalProject.graph_generator(number_of_nodes, connectedness_of_graph, name_of_test_file)
    AlgorithmsFinalProject.algorithms_final_project()