from googleapiclient.errors import HttpError
from django.conf import settings
import os
API_KEY = os.getenv('YOUTUBE_API_KEY', settings.YOUTUBE_API_KEY)
from googleapiclient.discovery import build

def get_youtube_comments(video_id):
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=100
        )
        response = request.execute()
        return response['items']
    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content}')
        return []
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return []