from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from googleapiclient.discovery import build

import os
import environ
import time
import re

env = environ.Env()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

class GoogleAuthenticate_API(APIView):
    def post(self, request):
        api_obj = build('youtube', 'v3', developerKey=env('YOUTUBE_APIKEY'))

        access_token = request.data['access_token']
        print(access_token)

        return(
            Response('pass')
        )