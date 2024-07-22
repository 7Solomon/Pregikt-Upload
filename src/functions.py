import subprocess, os
from datetime import datetime
import ffmpeg

from mutagen.id3 import ID3, TIT2, TALB, TPE1, TCON, TCOP, TYER, TDAT, TRDA, TLEN
from mutagen.mp3 import MP3

import json
import math
from pydub import AudioSegment

import ftplib
import requests
from bs4 import BeautifulSoup


def extract_date(filename):
    date_str = "-".join(filename.split('_')[0].split('-')[1:])  # Extracting '2024-06-08'
    return datetime.strptime(date_str, "%Y-%m-%d")

def compress_audio(file_name):
    input_file = f'{file_name}.mp3'
    out_path = os.path.join("file", "compressed_audio.mp3")
    
    # Get data
    threshold_db = check_config_file_for_key('threshold_db')
    ratio = check_config_file_for_key('ratio')
    attack = check_config_file_for_key('attack')
    release = check_config_file_for_key('release')

    # Convert -12 dB to amplitude ratio
    threshold_amplitude = math.pow(10, threshold_db / 20)
    

    (
        ffmpeg
        .input(input_file)
        .audio
        .filter('acompressor', threshold=threshold_amplitude, ratio=ratio, attack=attack, release=release)
        .output(out_path, acodec='libmp3lame', q=0)
        .overwrite_output()
        .run(capture_stdout=True, capture_stderr=True)
    )
    return out_path


def rename_file(file_name, datum):
    new_filename = f"file/predigt-{datum}_Treffpunkt_Leben_Karlsruhe.mp3"
    # Falls die Datei bereits existiert
    if os.path.exists(new_filename):
        os.remove(new_filename)
    os.rename(file_name, new_filename)
    return new_filename

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



def generate_id3_tags(file_path, prediger, predigt_titel, datum, year):

    audio = ID3(file_path)



    # Parse the date
    #year, month, day = datum.split('-')
    # Set the tags
    audio['TALB'] = TALB(encoding=3, text='Predigten aus Treffpunkt Leben Karlsruhe')
    audio['TCON'] = TCON(encoding=3, text='Predigt Online')
    audio['TCOP'] = TCOP(encoding=3, text='Treffpunkt Leben Karlsruhe - alle Rechte vorbehalten')
    audio['TIT2'] = TIT2(encoding=3, text=predigt_titel)
    audio['TPE1'] = TPE1(encoding=3, text=prediger)
    
    # Date tags
    audio['TYER'] = TYER(encoding=3, text=year)
    #audio['TDAT'] = TDAT(encoding=3, text=f"{day}{month}")
    audio['TRDA'] = TRDA(encoding=3, text=datum)  # This is the older equivalent of TDRC

    # Get audio duration
    mp3 = MP3(file_path)
    duration_ms = int(mp3.info.length * 1000)
    audio['TLEN'] = TLEN(encoding=3, text=str(duration_ms))

    # Save the changes
    audio.save(file_path)  # Explicitly save as ID3v2.3

    # Return the updated tags
    return dict(audio.items())


def send_file_to_server(path):
    file_name = os.path.basename(path)

    server = check_config_file_for_key('server')
    name = check_config_file_for_key('name')
    password = check_config_file_for_key('password')


    session = ftplib.FTP(server,name,password)
    file = open(path,'rb')              
    session.storbinary(f'STOR {file_name}', file)     # send the file
    file.close()                                    # close file and FTP
    session.quit()
    #return 'File uploaded to server'

def check_if_file_on_server(path):
    file_name = os.path.basename(path)

    server = check_config_file_for_key('server')
    name = check_config_file_for_key('name')
    password = check_config_file_for_key('password')
    try:
        # Connect to the FTP server
        session = ftplib.FTP(server, name, password)
        
        # Get list of files in the current directory on the server
        files_on_server = session.nlst()
        
        # Check if the file already exists on the server
        if file_name in files_on_server:
            #print(f"File '{file_name}' already exists on the server.")
            session.quit()
            return True
        else:
            #print(f"File '{file_name}' does not exist on the server.")
            session.quit()
            return False
        

    except ftplib.all_errors as e:
        print(f"Error: {e}")
        return

def get_audio_duration(file_path):
    audio = AudioSegment.from_file(file_path)
    print(f"Audio length: {len(audio)}")

    duration_seconds = len(audio) / 1000  # Duration in seconds
    duration_milliseconds = len(audio)  # Duration in milliseconds
    print(f"Duration: {duration_seconds} seconds ({duration_milliseconds} milliseconds)")
    return str(len(audio))

def get_themes_of_predigten():
    url = check_config_file_for_key('website_url')
    
    # At the time just for compiler
    if not url:
        return []
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find table
    table = soup.select_one("#predigt_main > table")
    themen = []
    if table:
        # Process the table
        rows = table.find_all('tr')
        for row in rows[1:7]:  # Skip header row, get next 3 rows
            columns = row.find_all('td')
            if len(columns) > 1:  # Ensure there's a theme column
                thema = columns[1].text.strip()
                thema = thema.replace("Thema:", "").strip()  # Remove some stuff
                themen.append(thema)  # Assuming theme is in the second column

    else:
        print("Table not found")
    
    return themen

def check_config_file_for_key(key):
    if not os.path.exists('config.json'):
        with open('config.json', 'w') as json_file:
            json.dump({"config_json_not_empty": "False"}, json_file)
    
    with open('config.json') as config_file:
        config = json.load(config_file)
        return config.get(key, None)

            


