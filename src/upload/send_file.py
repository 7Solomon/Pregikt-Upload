
import os
import ftplib
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from io import BytesIO
import requests

from utils import * 

def send_file_to_server(path):
    file_name = os.path.basename(path)

    server = check_config_file_for_key('server')
    name = check_config_file_for_key('name')
    password = check_config_file_for_key('password')


    session = ftplib.FTP(server,name,password)
    file = open(writable_path(path),'rb')              
    session.storbinary(f'STOR {file_name}', file)     # send the file
    file.close()                                    # close file and FTP
    session.quit()
    send_update_request()
    #return 'File uploaded to server'

def send_update_request():
    ### testPending
    url = check_config_file_for_key('update_url')
    
    if url:
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            print("Request was successful!")
            print("Response content:")
            print(response.text)  # Print the content of the response
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

def check_if_file_on_server(path):
    file_name = os.path.basename(writable_path(path))

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
    

def get_id3_tags_from_ftp(file_name):

    # Get data
    server = check_config_file_for_key('server')
    username = check_config_file_for_key('name')
    password = check_config_file_for_key('password')


    # Connect to FTP server
    ftp = ftplib.FTP(server)
    ftp.login(username, password)

    # Download part of the file to a BytesIO object
    file_like_object = BytesIO()
    ftp.retrbinary(f"RETR {file_name}", file_like_object.write)
    
    # Close the FTP connection
    ftp.quit()

    # Move to the beginning of the BytesIO object for reading
    file_like_object.seek(0)

    # Use mutagen to load and read the ID3 tags
    try:
        audio = MP3(file_like_object, ID3=ID3)
        for tag, value in audio.tags.items():
            print(f"{tag}: {value}")
    except Exception as e:
        print(f"Error reading ID3 tags: {e}")

