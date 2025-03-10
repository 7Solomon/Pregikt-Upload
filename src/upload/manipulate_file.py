
import  os
import tempfile
import ffmpeg
import math

from mutagen.id3 import ID3, TIT2, TALB, TPE1, TCON, TCOP, TYER, TDAT, TRDA, TLEN
from mutagen.mp3 import MP3


from utils import * 


def generate_id3_tags(file_name, prediger, predigt_titel, datum, year):

    audio = ID3(file_name)
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
    mp3 = MP3(file_name)
    duration_ms = int(mp3.info.length * 1000)
    audio['TLEN'] = TLEN(encoding=3, text=str(duration_ms))

    # Save the changes
    audio.save(file_name)  # Explicitly save as ID3v2.3

    # Return the updated tags
    return dict(audio.items())

def change_predigt_title(file_path,predigt_titel):
    audio = ID3(writable_path(file_path))
    audio['TIT2'] = TIT2(encoding=3, text=predigt_titel)
    audio.save(writable_path(file_path))
    return dict(audio.items())

def change_prediger(file_path,prediger):
    audio = ID3(writable_path(file_path))
    audio['TPE1'] = TPE1(encoding=3, text=prediger)
    audio.save(writable_path(file_path))
    return dict(audio.items())




def compress_audio(file_name):
    #input_file = f'{file_name}.mp3'
    #out_path = os.path.join("file", "compressed_audio.mp3")
    
    # Get data
    threshold_db = check_config_file_for_key('threshold_db')
    ratio = check_config_file_for_key('ratio')
    attack = check_config_file_for_key('attack')
    release = check_config_file_for_key('release')

    temp_file = tempfile.NamedTemporaryFile(suffix='.mp3',delete=False)
    
    # Convert -12 dB to amplitude ratio
    threshold_amplitude = math.pow(10, threshold_db / 20)
    try:
        result = (
            ffmpeg
            .input(file_name)
            .audio
            .filter('acompressor', threshold=threshold_amplitude, ratio=ratio, attack=attack, release=release)
            .output(temp_file.name, acodec='libmp3lame', q=0)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        print("FFmpeg stderr:", result[1].decode())
        os.unlink(file_name)
        
        return temp_file.name

    except ffmpeg.Error as e:
        print("FFmpeg stderr:", e.stderr.decode())
        os.unlink(file_name)
        raise

def rename_file(temp_file_name, datum):
    """Convert temporary file to permanent"""
    new_filename = f"stored/predigt-{datum}_Treffpunkt_Leben_Karlsruhe.mp3"
    new_writable_path = writable_path(new_filename)
    os.makedirs(os.path.dirname(new_writable_path), exist_ok=True)
    
    # Copy content from temp file to new permanent file
    with open(temp_file_name, 'rb') as temp_file:
        with open(new_writable_path, 'wb') as new_file:
            new_file.write(temp_file.read())
    # Clean up temp file
    os.unlink(temp_file_name)
    return new_writable_path