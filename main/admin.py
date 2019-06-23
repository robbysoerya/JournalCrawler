from django.contrib import admin
from main.models import ScrapyItem,Journal,Article,Author,References

class ScrapyAdmin(admin.ModelAdmin):
    list_display = ('data',)

# Register your models here.
admin.site.register(ScrapyItem,ScrapyAdmin)
admin.site.register(Journal)
admin.site.register(Article)

admin.site.register(Author)
admin.site.register(References)
