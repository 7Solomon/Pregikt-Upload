from pathlib import Path
import sys
from PyQt6 import QtWidgets as qtw

from src.utils import *
from src.upload.youtube import *
from src.windows.mainWindow import MainWindow

from src import server


### For Installer
BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)  # Change the working directory to BASE_DIR

def test():
    #data = get_last_livestream_data()
    server.app.run(debug=True)
    

def main():

    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    




if __name__ == '__main__':
    #test()
    main()
