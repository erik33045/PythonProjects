# noinspection PyUnresolvedReferences
import AlgorithmsGraphProject
import Stega_saurus

if '__main__' == __name__:
    AlgorithmsGraphProject.solve_maze()
    Stega_saurus.main(["embed", "input.txt", "atlas-x.png"])
    Stega_saurus.main(["extract", "atlas-secret.png"])