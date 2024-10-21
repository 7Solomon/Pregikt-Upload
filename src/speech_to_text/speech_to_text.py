import deepspeech
import numpy as np
import wave
import os
from pydub import AudioSegment
import io
from tqdm import tqdm


from utils import check_config_file_for_key

def speech_to_text(audio_file):
    # get model and Audio
    model_path = os.path.join('src','speech_to_text', 'deep_model.pbmm')
    model = deepspeech.Model(model_path)
    wav_data = convert_mp3_to_wav(audio_file)

    # Convert bytes to wave object
    wav_io = io.BytesIO(wav_data)
    with wave.open(wav_io, 'rb') as w:
        frames = w.getnframes()
        buffer = w.readframes(frames)
        data16 = np.frombuffer(buffer, dtype=np.int16)

    print("Starting transcription...")
    # Initialize progress bar
    chunk_size = 2048
    total_chunks = len(data16) // chunk_size
    text = ''
    
    for i in tqdm(range(0, len(data16), chunk_size), desc="Transcribing"):
        chunk = data16[i:i + chunk_size]
        text += model.stt(chunk)
    
    print("Transcription completed.")
    print(text)
    return text
def convert_mp3_to_wav(mp3_file:str):
    """
    mp3_file: url to file
    Sollte schon auch obvios sein was die macht
    returns:  WAV audio data
    """
    # Load the mp3 file
    audio = AudioSegment.from_mp3(mp3_file)
    
    # Create a BytesIO object
    wav_io = io.BytesIO()
    
    # Export as wav to the BytesIO object
    audio.export(wav_io, format="wav")
    
    # Get the wav data
    wav_data = wav_io.getvalue()
    return wav_data