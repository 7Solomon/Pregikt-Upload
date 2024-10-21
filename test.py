from mutagen.id3 import ID3, TIT2, TALB, TPE1, TCON, TCOP, TYER, TDAT, TRDA, TLEN
from mutagen.mp3 import MP3
from mutagen import File
from mutagen.easyid3 import EasyID3

import os
from src.speech_to_text.speech_to_text import speech_to_text
from src.speech_to_text.llama import *


from utils import get_themes_of_predigten

def print_audio_tags(file_path):
    try:
        # Try to open the file with Mutagen
        audio = File(file_path)
        
        if audio is None:
            print("File format not recognized by Mutagen.")
            return
        
        # If it's an MP3 file, we might need to use ID3 specifically
        if isinstance(audio, ID3):
            for key in audio.keys():
                print(f"{key}: {audio[key]}")
        else:
            # For other formats, we can just iterate through the tags
            for key in audio.tags.keys():
                print(f"{key}: {audio.tags[key]}")
                
    except Exception as e:
        print(f"An error occurred: {e}")

def print_mp3_tags(file_path):
    try:
        audio = MP3(file_path, ID3=EasyID3)
        print(len(audio.keys()))
        for key in audio.keys():
            print(f"{key}: {audio[key]}")
    except Exception as e:
        print(f"An error occurred: {e}")




def test():
    prompt = 'Was ist eine Maus?',
    pipeline, tokenizer = load_llam()
    use_llama(pipeline, tokenizer, prompt)

    #audio_file_path = os.path.join('stored', 'test.mp3')
    #speech_to_text(audio_file_path)
    
    
    
    #print_mp3_tags("stored\predigt-2024-07-14_Treffpunkt_Leben_Karlsruhe.mp3")



if __name__ == "__main__":
    test()