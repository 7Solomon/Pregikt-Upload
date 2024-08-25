
import  os
import ffmpeg
import math

from mutagen.id3 import ID3, TIT2, TALB, TPE1, TCON, TCOP, TYER, TDAT, TRDA, TLEN
from mutagen.mp3 import MP3


from src.utils import * 


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

def change_predigt_title(file_path,predigt_titel):
    audio = ID3(file_path)
    audio['TIT2'] = TIT2(encoding=3, text=predigt_titel)
    audio.save(file_path)
    return dict(audio.items())

def change_prediger(file_path,prediger):
    audio = ID3(file_path)
    audio['TPE1'] = TPE1(encoding=3, text=prediger)
    audio.save(file_path)
    return dict(audio.items())




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