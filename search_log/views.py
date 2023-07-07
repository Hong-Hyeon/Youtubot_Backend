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
        temp = {}

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

            for items in response['items']:
                reply = items['snippet']['topLevelComment']['snippet']['textDisplay']
                author = items['snippet']['topLevelComment']['snippet']['authorDisplayName']

                temp[author] = reply

            predict_obj = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role':'user', 'content':'{} \n 이 json데이터의 value를 평가할거야. 1~5점 중 가장 긍정적인 점수를 5점으로 하고 가장 부정적인 점수를 1점으로 했을 때, 너의 생각에는 value는 각각 몇점이야? 판단하기 어려운 value가 있다면 -1을 줘'.format(temp)}
                ]
            )
            
            print((predict_obj.choices[0].message.content).split(','))
            for item in (predict_obj.choices[0].message.content).split(','):
                item = item.split(':')

                score = re.sub(r"[^0-9]",'',item[1])
                author = re.sub(r"[%$^*!{}'\n ]", '', item[0])

                for temp_author, reply in temp.items():
                    if author == temp_author:
                        response_obj[author] = {reply:score}
                print(response_obj)

            return Response(
                response_obj
            )
            # return Response(
            #     ReviewSerializer(new_review).data,
            # )
        else:
            return Response(serializer.errors)