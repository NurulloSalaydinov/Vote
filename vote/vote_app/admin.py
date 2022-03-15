from django.contrib import admin
from .models import *

admin.site.register(TelegramUser)
@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
	list_display = ("id", "title")
	search_fields = ("title",)
	prepopulated_fields = {'slug':('title',)}
admin.site.register(Category)
admin.site.register(CategoryItem)

