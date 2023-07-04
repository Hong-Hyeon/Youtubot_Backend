from rest_framework import serializers

from .models import SearchLog

class SearchLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchLog
        fields = "__all__"