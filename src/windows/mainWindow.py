from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QPushButton, 
                            QLabel, QWidget, QScrollArea, QHBoxLayout, 
                            QProgressBar, QStackedWidget, QLineEdit, QTextEdit, 
                            QCalendarWidget, QComboBox, QFrame,QGroupBox, QSizePolicy,
                            QProgressBar, QMessageBox)
from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import QFont

from utils import *
from src.windows.overviewWidget import OverviewWidget
from src.windows.worker import *
from src.windows.detailWidget import DetailWidget
from src.windows.loginWidget import LoginWidget

import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hochladen der Predigt')
        self.setGeometry(100, 100, 750, 350)

        # Define Structure
        self.stackedWidget = QStackedWidget()

        self.mainWidget = QWidget()
        self.stackedWidget.addWidget(self.mainWidget)
        self.setCentralWidget(self.stackedWidget)

        self.config_Widget = LoginWidget(self.stackedWidget, self)
        self.stackedWidget.addWidget(self.config_Widget)
        

        # Check if structure is correct
        if not os.path.exists(writable_path('stored')):
            os.mkdir(writable_path('stored'))
        if not os.path.exists(writable_path('file')):
            os.mkdir(writable_path('file'))




        self.init_app()
        # Look if config Json file
        config_json_not_empty = check_config_file_for_key('config_json_not_empty')
        
        if config_json_not_empty == None or config_json_not_empty == "False":
           self.stackedWidget.setCurrentWidget(self.config_Widget)


    def init_app(self):      
        self.mainLayout = QVBoxLayout()  

        self.debug = QLabel("")
        self.debug.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.debug.setStyleSheet("""
            color: #000000;
            background-color: #f0f0f0;
            border: 2px solid #3498db;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        """)
        self.mainLayout.addWidget(self.debug)


        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.content = QWidget()
        self.contentLayout = QVBoxLayout(self.content)

        self.scroll.setWidget(self.content)
        self.mainLayout.addWidget(self.scroll)

        self.buttonLayout = QHBoxLayout()
        self.dataButton = QPushButton("Get Data")
        self.dataButton.clicked.connect(self.loadData)
        self.dataButton.setFixedSize(100, 60)
        self.buttonLayout.addWidget(self.dataButton)
        self.overviewButton = QPushButton("Direkt zum Overview")
        self.overviewButton.clicked.connect(self.toOverview)
        self.overviewButton.setFixedSize(160, 40)
        self.buttonLayout.addWidget(self.overviewButton)

        self.progressBar = QProgressBar()
        self.progressBar.setVisible(False)
        self.buttonLayout.addWidget(self.progressBar)

        self.mainLayout.addLayout(self.buttonLayout)
        self.mainWidget.setLayout(self.mainLayout)


        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.updateUI)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

    def loadData(self):
        try:
            self.progressBar.setVisible(True)
            self.progressBar.setRange(0, 0)
            self.thread.start()
        except Exception as e:
            self.debug.setText(e)

    def updateUI(self, data):
        self.progressBar.setVisible(False)
        self.progressBar.setRange(0, 100)
        for item in data:
            btn = QPushButton(item['title'])
            btn.setStyleSheet("QPushButton { font-size: 16px; padding: 10px; }")
            btn.clicked.connect(lambda checked, item=item: self.showDetailWidget(item))
            self.contentLayout.addWidget(btn)

    def showDetailWidget(self, item):
        detailWidget = DetailWidget(item, self.stackedWidget, self)
        self.stackedWidget.addWidget(detailWidget)
        self.stackedWidget.setCurrentWidget(detailWidget)
    def toOverview(self):
        try:
            overviewWidget = OverviewWidget(self.stackedWidget, self)
            self.stackedWidget.addWidget(overviewWidget)
            self.stackedWidget.setCurrentWidget(overviewWidget)
        except Exception as e:
            self.debug.setText(e)