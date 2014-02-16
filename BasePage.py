import os
import cProfile
# noinspection PyUnresolvedReferences
import AlgorithmSortingProject as Asp

if '__main__' == __name__:
    os.remove("Hendrickson.txt")
    cProfile.run('Asp.algorithm_sorting_project()')