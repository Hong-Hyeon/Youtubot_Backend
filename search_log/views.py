from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from .models import SearchLog
from .serializers import SearchLogSerializer

from googleapiclient.discovery import build

import os
import environ
import openai
import time
import re

env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
openai.api_key = env('GPT_APIKEY')

class SearchLog_API(APIView):
    def get(self, request):
        all_log = SearchLog.objects.all()
        serializer = SearchLogSerializer(all_log, many=True)
        return Response(
            serializer.data
        )
    
    def post(self, request):
        response_obj = {}

        serializer = SearchLogSerializer(data = request.data)
        if serializer.is_valid():
            # new_searchlog = serializer.save()

            target_link = request.data['search_link']
            youtube_ids = target_link.split('/')
            for target in youtube_ids:
                infos = target.split('&')
                for info in infos:
                    if 'watch?v=' in info:
                        media_id = info.split('=')[1]
            if media_id is False:
                return SearchLog.DoesNotExist
            
            api_obj = build('youtube', 'v3', developerKey=env('YOUTUBE_APIKEY'))
            response = api_obj.commentThreads().list(part='snippet,replies', videoId=media_id, maxResults=100).execute()

            # print(len(response['items']))
            for items in response['items']:
                reply = items['snippet']['topLevelComment']['snippet']['textDisplay']
                author = items['snippet']['topLevelComment']['snippet']['authorDisplayName']

                predict_obj = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=[
                        {'role':'user', 'content':'"{}"라는 글을 가장 긍정적인 점수 5에서 가장 부정적인 점수 1까지로 점수를 내면 몇점이야? 단답으로 점수만 말해줘'.format(reply)}
                    ]
                )
                predict_reply = re.sub(r'[^0-9]','',predict_obj.choices[0].message.content)
                time.sleep(0.5)

                response_obj[author] = {'reply':reply, 'positive_rating':predict_reply}

            return Response(
                response_obj
            )
            # return Response(
            #     ReviewSerializer(new_review).data,
            # )
        else:
            return Response(serializer.errors)