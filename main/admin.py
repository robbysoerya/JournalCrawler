from django.contrib import admin
from main.models import ScrapyItem

class ScrapyAdmin(admin.ModelAdmin):
    list_display = ('data',)

# Register your models here.
admin.site.register(ScrapyItem, ScrapyAdmin)