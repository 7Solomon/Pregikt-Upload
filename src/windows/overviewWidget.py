from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QPushButton, 
                            QLabel, QWidget, QScrollArea, QHBoxLayout, 
                            QProgressBar, QStackedWidget, QLineEdit, QTextEdit, 
                            QCalendarWidget, QComboBox, QFrame,QGroupBox, QSizePolicy,
                            QProgressBar, QMessageBox)
from PyQt6.QtCore import Qt, QThread

from src.functions import *
from src.windows.worker import *

import os
from datetime import datetime





class OverviewWidget(QWidget):
    def __init__(self, stackedWidget, parent=None):
        super().__init__(parent)
        self.stackedWidget = stackedWidget
        self.layout = QVBoxLayout()


        # Initialize dictionaries to keep track of workers and threads
        self.workers = {}
        self.threads = {}

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

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollContent = QWidget()
        self.scrollLayout = QVBoxLayout(self.scrollContent)

        self.scrollArea.setWidget(self.scrollContent)
        self.layout.addWidget(self.scrollArea)

        self.setLayout(self.layout)
        self.create_overview()

    def create_overview(self):        
        if os.path.exists('stored'):
            dir = os.listdir('stored/')
        else:
            os.mkdir('stored')
            dir = os.listdir('stored/')
        
        # Filter and sort files based on their names (assuming the date is part of the file name)

        ### Problem in here, if file with not possible extract_date it returns an error
        filtered_files = sorted(dir, key=extract_date, reverse=True)[:5]
        

        for i, file_name in enumerate(filtered_files):
            file_item = QPushButton(file_name)
            file_item.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            file_item.setStyleSheet(f"""
                QPushButton {{
                    border: 1px solid gray;
                    border-radius: 5px;
                    padding: 10px;
                    background-color: {"lightgreen" if check_if_file_on_server(file_name) else "lightcoral"};
                }}
                QPushButton:pressed {{
                    background-color: gray;
                }}
            """)
            file_item.clicked.connect(lambda checked, name=file_name, item=file_item: self.handle_file_click(name, item))
            self.scrollLayout.addWidget(file_item)
    
    def update_overview(self):
        for i in range(self.scrollLayout.count()):
            widget_to_Update = self.scrollLayout.itemAt(i).widget()
            file_name = widget_to_Update.text()
            widget_to_Update.setStyleSheet(f"""
                QPushButton {{
                    border: 1px solid gray;
                    border-radius: 5px;
                    padding: 10px;
                    background-color: {"lightgreen" if check_if_file_on_server(file_name) else "lightcoral"};
                }}
                QPushButton:pressed {{
                    background-color: gray;
                }}
            """)

    def handle_file_click(self, file_name, file_item):
        try:    
            file_item.setEnabled(False)
            self.start_file_upload(file_name, file_item)
        except Exception as e:
            self.debug.setText(e)

    def start_file_upload(self, file_name, file_item):
        path = f'stored/{file_name}'
        worker = UploadWorker(path)
        thread = QThread()

        # Store worker and thread in dictionaries
        self.workers[file_name] = worker
        self.threads[file_name] = thread

        worker.moveToThread(thread)

        # Add Progress Bar
        #progress_bar = self.scrollLayout.itemAt(i + 1).widget()

        # Connect signals
        worker.finished.connect(lambda: self.upload_finished(file_name, file_item))

        thread.started.connect(worker.run)
        thread.start()

    def update_progress(self,file_name, value):
        pass


    def upload_finished(self, file_name ,file_item):
        file_item.setEnabled(True)
        QMessageBox.information(self, "Upload Complete", f"{file_name} has been uploaded.")
        self.update_overview()

