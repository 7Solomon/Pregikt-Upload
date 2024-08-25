import os
from datetime import datetime
import json



def extract_date(filename):
    date_str = "-".join(filename.split('_')[0].split('-')[1:])  # Extracting '2024-06-08'
    return datetime.strptime(date_str, "%Y-%m-%d")


def manage_files(dir_name):
    dir = os.listdir('file/')
    if dir.__contains__('pre_compressed_audio.mp3'):
        os.remove('file/pre_compressed_audio.mp3')
    if dir.__contains__('file/compressed_audio.mp3'):
        os.remove('file/compressed_audio.mp3')
 
    file_name = dir_name.split('/')[1]
    
    if os.path.exists(dir_name):
        # Remove if file already exists
        if os.path.exists(f'stored/{file_name}'):
            os.remove(f'stored/{file_name}')

        os.rename(dir_name, f'stored/{file_name}')
        return f'stored/{file_name}'
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
    if not os.path.exists('config.json'):
        with open('config.json', 'w') as json_file:
            json.dump({"config_json_not_empty": "False"}, json_file)
    
    with open('config.json') as config_file:
        config = json.load(config_file)
        return config.get(key, None)

            


