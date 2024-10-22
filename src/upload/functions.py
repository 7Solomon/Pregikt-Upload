import os
from src import *
from utils import writable_path


def init():
    # Check if structure is correct
    if not os.path.exists(writable_path('stored')):
        os.mkdir(writable_path('stored'))
    if not os.path.exists(writable_path('file')):
        os.mkdir(writable_path('file'))

def check_config_file():
    pass