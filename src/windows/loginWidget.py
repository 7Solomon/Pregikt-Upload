from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QLabel, QWidget, QMessageBox, QPushButton)
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
import json

from src.functions import *
from src.windows.overviewWidget import OverviewWidget
from src.windows.worker import *
from src.windows.detailWidget import DetailWidget


class LoginWidget(QWidget):
    def __init__(self, stacked_widget, parent: QWidget):
        super().__init__(parent)
        self.stacked_widget = stacked_widget

        self.layout = QVBoxLayout()
        self.label = QLabel("Drag and drop, JSON file hier!")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

        self.back_button = QPushButton("Zurück")
        self.back_button.clicked.connect(self.get_back)
        self.back_button.setVisible(False)
        self.layout.addWidget(self.back_button)
        self.setLayout(self.layout)

        # Enable drag and drop
        self.setAcceptDrops(True)
    
    def get_back(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.widget(0))

    def dragEnterEvent(self, event: QDragEnterEvent):
        # Check if the dragged data is a file and if it is a JSON file
        if event.mimeData().hasUrls() and all(url.isLocalFile() for url in event.mimeData().urls()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragEnterEvent):
        # Accept the move event if the data is correct
        if event.mimeData().hasUrls() and all(url.isLocalFile() for url in event.mimeData().urls()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        # Process the dropped file
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith(".json"):
                self.process_file(file_path)
            else:
                QMessageBox.warning(self, "Invalid File", "Please drop a JSON file.")
    
    def process_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Write the contents to config.json
            with open('config.json', 'w') as config_file:
                json.dump(data, config_file, indent=4)
                
            self.label.setText("Erfolgreich config.json configuriert!")
            self.back_button.setVisible(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load JSON file: {e}")
