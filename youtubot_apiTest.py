from googleapiclient.discovery import build

import os
import environ

env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

comments = list()
api_obj = build('youtube', 'v3', developerKey=env('YOUTUBE_APIKEY'))
response = api_obj.commentThreads().list(part='snippet,replies', videoId='Y54FNviigS8', maxResults=100).execute()

print(response)