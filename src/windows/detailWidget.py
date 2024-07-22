from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QPushButton, 
                            QLabel, QWidget, QScrollArea, QHBoxLayout, 
                            QProgressBar, QStackedWidget, QLineEdit, QTextEdit, 
                            QCalendarWidget, QComboBox, QFrame,QGroupBox, QSizePolicy,
                            QProgressBar, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.functions import *
from src.windows.overviewWidget import OverviewWidget
from src.windows.worker import *




class DetailWidget(QWidget):
    def __init__(self, item, stackedWidget, parent=None):
        super().__init__(parent)
        self.item = item
        self.stackedWidget = stackedWidget
        self.layout = QVBoxLayout()

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
        self.layout.addWidget(self.debug)


        
        self.titleLabel = QLabel(f"{item['title']}")
        self.titleLabel.setFont(QFont("Arial", 16))
        self.titleLabel.setWordWrap(True)  # Allow the text to wrap over multiple lines
        self.titleLabel.setMaximumWidth(600)  # Limit the maximum width
        self.titleLabel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)  # Set size policy
        self.titleLabel.setMinimumHeight(50)  # Set the minimum height
        headlineGroupBox = QGroupBox()  # You can change the name here
        headlineGroupBox.setStyleSheet("QGroupBox { border: 1px solid gray; border-radius: 10px; }")
        groupBoxLayout = QVBoxLayout(headlineGroupBox)
        groupBoxLayout.addWidget(self.titleLabel)

        self.layout.addWidget(headlineGroupBox)

        self.wrapperWidget = QWidget()
        self.wrapperLayout = QHBoxLayout(self.wrapperWidget)

        self.groupBox = QGroupBox("Name der Predigt")
        self.groupBox.setStyleSheet("""
            QGroupBox { 
                border: 1px solid gray; 
                border-radius: 5px; 
                padding-top: 10px; 
                padding-left: 10px; 
            }
        """)
        self.groupBoxLayout = QVBoxLayout(self.groupBox)
        self.groupBox.setFixedSize(450, 120)

        # Create a QComboBox
        self.predigt_box = QComboBox()
        self.predigt_box.setEditable(True) 
        self.predigt_box.setFixedSize(400, 60)

        try:
            # Populate the QComboBox with suggestions if is defined
            website_exists = check_config_file_for_key('website_exists')
            if website_exists:
                suggestions = ["", *get_themes_of_predigten()]
            else:
                suggestions = [""]
            
            self.predigt_box.addItems(suggestions)
            self.groupBoxLayout.addWidget(self.predigt_box)
        except Exception as e:
            self.debug.setText(str(e))

        #self.lineEdit = QLineEdit()
        #self.groupBoxLayout.addWidget(self.lineEdit)

        self.wrapperLayout.addWidget(self.groupBox)

        self.audioLengthLabel = QLabel()
        self.audio_length = item['length']
        self.display_audio_length()
        self.wrapperLayout.addWidget(self.audioLengthLabel)


        self.layout.addWidget(self.wrapperWidget)

        self.comboBox = QComboBox()
        self.comboBox.setEditable(True)
        self.comboBox.addItems(["Philipp Hönes", "Timon Kaiser", "Gernot Elsner", "Timon Heuser", "Benjamin Rohland", " --- "])
        self.comboBox.setFixedSize(300, 50)
        self.layout.addWidget(self.comboBox)

        self.calendar = QCalendarWidget(self) 
        self.calendar.setFixedSize(600, 300)
        self.layout.addWidget(self.calendar)
        
        # Add padding
        paddingWidget = QWidget()
        paddingWidget.setFixedSize(600, 20)  # Adjust the height as needed for the desired padding
        self.layout.addWidget(paddingWidget)
        
        self.baseContainerWidget = QWidget()
        self.baseContainerLayout = QHBoxLayout(self.baseContainerWidget)
        
        

        self.submitButton = QPushButton("Erstellen", self)
        self.submitButton.clicked.connect(self.handleSubmit)
        self.submitButton.setFixedSize(100, 60)
        self.baseContainerLayout.addWidget(self.submitButton, alignment=Qt.AlignmentFlag.AlignCenter)  # Align the button to the center


        # Add the progress bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setFixedSize(600, 30)
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)
        self.baseContainerLayout.addWidget(self.progressBar)


        self.layout.addWidget(self.baseContainerWidget)


        self.setLayout(self.layout)

    def handleSubmit(self):
        try:
            self.submitButton.setVisible(False)
            self.submitButton.setEnabled(False)
            self.progressBar.setVisible(True)
            self.progressBar.setValue(0)
            self.workerThread = WorkerThread(self.item, self.comboBox.currentText(), self.predigt_box.currentText(), self.calendar.selectedDate())
            self.workerThread.progress.connect(self.updateProgressBar)
            self.workerThread.finished.connect(self.onProcessFinished)
            self.workerThread.error.connect(self.onPrecessError)
            self.workerThread.start()
        except Exception as e:
            self.debug.setText(str(e))

    def updateProgressBar(self, value):
        self.progressBar.setValue(value)

    def onProcessFinished(self, result):

        self.submitButton.setEnabled(True)
        self.submitButton.setVisible(True)        
        self.showOverviewWidget()

    def onPrecessError(self,result):
        self.progressBar.setValue(0)
        self.submitButton.setVisible(False)  

        self.debug.setText(result)


    
    def showOverviewWidget(self):
        overviewWidget = OverviewWidget(self.stackedWidget, self)
        self.stackedWidget.addWidget(overviewWidget)
        self.stackedWidget.setCurrentWidget(overviewWidget)

    def display_audio_length(self):
        audioLengthLabel = QLabel()
        audioLengthLabel.setText(f'Die Predigt ist wahrscheinlich schon Geschnitten, da die Audiolänge {time_to_seconds(self.audio_length)} beträgt')
        audioLengthLabel.setFont(QFont("Arial", 12))
        audioLengthLabel.setStyleSheet("""
            QLabel {
                border: 2px solid gray;
                border-radius: 5px;
                padding: 5px;
                background-color: lightblue;
            }
        """)
        if self.audio_length > 3600000:  # 1 hour = 3600000 milliseconds
            audioLengthLabel.setStyleSheet("""
                QLabel {
                    border: 2px solid gray;
                    border-radius: 5px;
                    padding: 5px;
                    background-color: lightcoral;
                }
            """)
            audioLengthLabel.setText(f'Die Predigt ist wahrscheinlich noch NICHT Geschnitten, da die Audiolänge {time_to_seconds(self.audio_length)} beträgt')

        self.wrapperLayout.addWidget(audioLengthLabel)
