import json
from yt_dlp import YoutubeDL
from googleapiclient.discovery import build
import isodate

from src.functions import check_config_file_for_key


api_key = check_config_file_for_key('YOUTUBE_API_KEY')
if api_key:
    youtube = build('youtube', 'v3', developerKey=api_key)
else:
    youtube = None

def get_youtube_data():
    global youtube 
    if not youtube:
        api_key = check_config_file_for_key('YOUTUBE_API_KEY')
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
        maxResults=3
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
                startTime = livestream_info['liveStreamingDetails']['actualStartTime']
                duration = get_video_duration(livestream_info['id'])
                if duration is None:
                    duration = 'Length not available'
                URL = f"https://www.youtube.com/watch?v={video_id}"
                last_livestreams.append({"title": title, "description": description, "startTime": startTime, "URL": URL, 'length':duration})

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

    download_options = {
        'format': 'bestaudio/best',
        'outtmpl': 'file/pre_compressed_audio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(download_options) as ydl:
        ydl.download([URL])
    
    
    return 'file/pre_compressed_audio'

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