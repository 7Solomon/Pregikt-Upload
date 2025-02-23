import json
from yt_dlp import YoutubeDL
from googleapiclient.discovery import build
import isodate

import tempfile

from utils import * 


api_key = check_config_file_for_key('YOUTUBE_API_KEY')
if api_key:
    youtube = build('youtube', 'v3', developerKey=api_key)
else:
    youtube = None

def get_last_livestream_data(limit = 20):
    global youtube 
    if not youtube:
        api_key = check_config_file_for_key('YOUTUBE_API_KEY')
        print(api_key)
        youtube = build('youtube', 'v3', developerKey=api_key)

    channel_id = check_config_file_for_key('channel_id')
    parts_to_retrieve = "contentDetails"

    # ContentDeta des Chanels
    channel_response = youtube.channels().list(
        id=channel_id,
        part=parts_to_retrieve
    ).execute()

    uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Latest Playist
    playlist_response = youtube.playlistItems().list(
        playlistId=uploads_playlist_id,
        part='contentDetails',
        maxResults=limit      #!!! Hier kann geändert werden wie viele Videos zurückgegeben werden sollen
    ).execute()


    if 'items' in playlist_response and playlist_response['items']:

        last_livestreams = []
        for item in playlist_response['items']:
            video_id = item['contentDetails']['videoId']



            # Livestream Details
            video_response = youtube.videos().list(
                id=video_id,
                part='snippet,liveStreamingDetails'
            ).execute()

            # Check if the video is live
            if 'liveStreamingDetails' in video_response['items'][0]:
                livestream_info = video_response['items'][0]
                
                for key, value in livestream_info.items():
                    if isinstance(value, dict):
                        for key, value in value.items():
                            print(f"{key}: {value}")
                    else:
                        print(f"{key}: {value}")

                title =  livestream_info['snippet']['title']
                description = livestream_info['snippet']['description']
                print(livestream_info['liveStreamingDetails'].keys())

                #startTime = livestream_info['liveStreamingDetails']['actualStartTime']
                duration = get_video_duration(livestream_info['id'])
                if duration is None:
                    duration = 'Length not available'
                URL = f"https://www.youtube.com/watch?v={video_id}"
                #last_livestreams.append({"title": title, "description": description, "startTime": startTime, "URL": URL, 'length':duration})
                last_livestreams.append({"title": title, "description": description, "URL": URL, 'length':duration})

            else:
                print("Das Letzte Video ist kein Livestream")
                
        else:
            print("Die Playlist hat leider keine Videos")
    return last_livestreams


def dowload_youtube(URL):
    global youtube 
    if not youtube:
        api_key = check_config_file_for_key('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
    
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file_name = f'{temp_file.name}.mp3'
    temp_file.close()  # Close the file but keep it on disk

    
    download_options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{temp_file.name}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        
        'verbose': True, # FOR DEBUGGING
        'keepvideo': False,
        'overwrites': True,
        'ffmpeg_location': None 
    }

    try:
        with YoutubeDL(download_options) as ydl:
            print(f"Downloading to: {temp_file_name}")
            ydl.download([URL])
            return temp_file_name
    except Exception as e:
        print(f"Download error: {str(e)}")
        # Cleanup any temporary files
        for ext in ['.mp3', '.webm', '.m4a', '.part']:
            possible_file = f"{temp_file_name}{ext}"
            if os.path.exists(possible_file):
                os.unlink(possible_file)
        raise

def get_video_duration(video_id):

    video_response = youtube.videos().list(
        part='contentDetails',
        id=video_id
    ).execute()

    if 'items' in video_response and len(video_response['items']) > 0:
        content_details = video_response['items'][0]['contentDetails']
        duration = content_details['duration']
        duration= isodate.parse_duration(duration).total_seconds() * 1000
        return duration
    else:
        return None



if __name__ == '__main__':
    pass