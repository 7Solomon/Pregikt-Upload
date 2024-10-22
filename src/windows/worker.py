from PyQt6.QtCore import Qt, pyqtSignal, QObject, QThread

from src.upload.youtube import get_last_livestream_data, dowload_youtube
from src.upload.send_file import *
from src.upload.manipulate_file import *
from utils import *


class Worker(QObject):
    finished = pyqtSignal(list)

    def run(self):
        data = get_last_livestream_data()
        self.finished.emit(data)


class UploadWorker(QThread):
    progress = pyqtSignal(int)  # Signal to emit progress updates (percentage)
    finished = pyqtSignal()     # Signal to indicate completion

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path

    def run(self):
        send_file_to_server(self.file_path)  # Assuming send_file_to_server is defined elsewhere
        self.progress.emit(100)  # Emit 100% progress when done
        self.finished.emit()    # Emit finished signal


class WorkerThread(QThread):
    progress = pyqtSignal(int)
    error = pyqtSignal(str)
    finished = pyqtSignal(str)

    def __init__(self, item, prediger, predigt_titel, datum, parent=None):
        super().__init__(parent)
        self.item = item
        self.prediger = prediger
        self.predigt_titel = predigt_titel
        self.datum = datum

    def run(self):
        try:
            # Download file from youtube
            file_url = dowload_youtube(self.item['URL'])
            self.progress.emit(20)

            # Compress File
            file_url = compress_audio(file_url)
            self.progress.emit(40)

            # Get Date
            datum_str = self.datum.toString(Qt.DateFormat.ISODate)
            year = self.datum.toString("yyyy")

            # Generate Tags
            generate_id3_tags(file_url, self.prediger, self.predigt_titel, datum_str, year)
            self.progress.emit(60)

            # Manage files
            file_url = rename_file(file_url, datum_str)
            self.progress.emit(80)
            manage_files(file_url)
            self.progress.emit(100)
            self.finished.emit(file_url)
        except Exception as e:
            self.error.emit(str(e))


class FileWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path = path

    def run(self):
        file_name = os.path.basename(self.path)
        server = check_config_file_for_key('server')
        name = check_config_file_for_key('name')
        password = check_config_file_for_key('password')

        session = ftplib.FTP(server, name, password)
        file = open(self.path, 'rb')

        # Get file size for progress calculation
        file_size = os.path.getsize(self.path)
        uploaded_bytes = 0

        def progress_callback(data):
            nonlocal uploaded_bytes
            uploaded_bytes += len(data)
            progress_percent = int(uploaded_bytes / file_size * 100)
            self.progress.emit(progress_percent)

        session.storbinary(f'STOR {file_name}', file, callback=progress_callback)
        file.close()
        session.quit()
        self.finished.emit()
