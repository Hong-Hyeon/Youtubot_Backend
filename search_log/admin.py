from django.contrib import admin
from .models import SearchLog

# Register your models here.
@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    
    list_display = ('search_link',)