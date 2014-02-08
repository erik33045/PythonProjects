import shutil

import UniversalExtractor


if '__main__' == __name__:
    shutil.rmtree('C:\Users\erik3_000\IdeaProjects\PythonBaseProject\Test')
    UniversalExtractor.universal_extractor("Test",
                                           ["Testtar.tar", "Testtarbz2.tar.bz2", "Testtargz.tar.gz", "Testtbz.tbz",
                                            "Testtgz.tgz", "Testtxtbz2.txt.bz2", "Testtxtgz.txt.gz", "Testzip.zip"])