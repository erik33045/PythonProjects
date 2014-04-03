# noinspection PyUnresolvedReferences
import datetime
import AlgorithmsGraphProject
import Stega_saurus
if '__main__' == __name__:
    AlgorithmsGraphProject.solve_maze()
    Stega_saurus.main(["x", "embed", "input2.txt", "atlas.png"])
    Stega_saurus.main(["x", "extract", "atlas-secret.png"])