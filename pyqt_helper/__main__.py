from sys import argv
from .pyqt_helper import main


try:
    main(argv)
except TypeError as e:
    print(e)
    exit(1)
