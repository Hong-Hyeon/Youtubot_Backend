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

env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

class SearchLog_API(APIView):
    def get(self, request):
        all_log = SearchLog.objects.all()
        serializer = SearchLogSerializer(all_log, many=True)
        return Response(
            serializer.data
        )
    
    def post(self, request):
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

            return Response(
                response
            )
            # return Response(
            #     ReviewSerializer(new_review).data,
            # )
        else:
            return Response(serializer.errors)