from django.db import models
from common.models import CommonModel

# Create your models here.
class SearchLog(CommonModel):

    search_link = models.TextField()