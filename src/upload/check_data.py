
from pydub import AudioSegment
import requests
from bs4 import BeautifulSoup

from utils import * 

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
