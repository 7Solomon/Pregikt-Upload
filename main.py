import sys
from PyQt6 import QtWidgets as qtw

from src.functions import *
from src.yt_download_latest_stream import *
from src.windows.mainWindow import MainWindow

def test():
    data = get_youtube_data()
    print(data)
    

def main():
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    




if __name__ == '__main__':
    main()
