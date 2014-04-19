# noinspection PyUnresolvedReferences
import datetime
import AlgorithmsFinalProject



if '__main__' == __name__:
    number_of_nodes = 1000
    connectedness_of_graph = 100
    name_of_test_file = "input2.txt"

    #AlgorithmsFinalProject.graph_generator(number_of_nodes, connectedness_of_graph, name_of_test_file)
    #AlgorithmsFinalProject.algorithms_final_project()

    #AlgorithmsFinalProject.adams_solution(name_of_test_file)
    AlgorithmsFinalProject.random_cut(name_of_test_file, 20)

