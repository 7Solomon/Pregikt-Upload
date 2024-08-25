import os
from src import *


def init():
    # Check if structure is correct
    if not os.path.exists('stored'):
        os.mkdir('stored')
    if not os.path.exists('file'):
        os.mkdir('file')

def check_config_file():
    pass