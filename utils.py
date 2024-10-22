import os
from datetime import datetime
import json
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
def writable_path(relative_path):
    """Get absolute path for a writable directory"""
    # Example: Store writable files in the user's home directory or AppData
    if sys.platform == "win32":
        writable_base = os.path.join(os.getenv('APPDATA'), 'PregiktUpload')
    else:
        writable_base = os.path.join(os.path.expanduser('~'), '.PregiktUpload')
    # Create the directory if it doesn't exist
    os.makedirs(writable_base, exist_ok=True)
    return os.path.join(writable_base, relative_path)

def extract_date(filename):
    date_str = "-".join(filename.split('_')[0].split('-')[1:])  # Extracting '2024-06-08'
    return datetime.strptime(date_str, "%Y-%m-%d")


def manage_files(dir_name):
    dir = os.listdir(writable_path('file/'))
    if dir.__contains__(writable_path('pre_compressed_audio.mp3')):
        os.remove(writable_path('file/pre_compressed_audio.mp3'))
    if dir.__contains__(writable_path('file/compressed_audio.mp3')):
        os.remove('file/compressed_audio.mp3')
 
    file_name = dir_name.split('/')[1]
    
    if os.path.exists(writable_path(dir_name)):
        # Remove if file already exists
        if os.path.exists(writable_path(f'stored/{file_name}')):
            os.remove(writable_path(f'stored/{file_name}'))

        os.rename(writable_path(dir_name), writable_path(f'stored/{file_name}'))
        return writable_path(f'stored/{file_name}')
    else:
        print('File not found')


def convert_ms(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return hours, minutes, seconds, milliseconds


def time_to_seconds(time_str):
    seconds = int(time_str)/1000
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)

    # Format the output with the required number of digits
    formatted_time = f"{hours:02}:{minutes:02}:{secs:02}"
    return formatted_time




def check_config_file_for_key(key):
    if not os.path.exists(writable_path('config.json')):
        with open(writable_path('config.json'), 'w') as json_file:
            json.dump({"config_json_not_empty": "False"}, json_file)
    
    with open(writable_path('config.json')) as config_file:
        config = json.load(config_file)
        return config.get(key, None)

            


