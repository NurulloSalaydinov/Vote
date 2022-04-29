from django.contrib import admin

from .models import Category, Places,BotUser,RegistredBotUser

from django.utils.html import mark_safe

# Register your models here.
class PlacesAdminTabularInline(admin.TabularInline):
    model = Places
    extra = 1

@admin.register(Category)
class CategoryAdminRegister(admin.ModelAdmin):
    list_display = ['id','name']
    list_editable = ['name']
    search_fields = ['name','id','date']
    inlines = [PlacesAdminTabularInline]

@admin.register(Places)
class PlacesAdminRegister(admin.ModelAdmin):
    list_display = ['id','name','vote']
    list_editable = ['name']
    search_fields = ['name','vote']
    list_filter = ['id']

@admin.register(BotUser)
class BotUserAdminRegister(admin.ModelAdmin):
    list_display = ['phonenumber','voted','telegram','call','date']
    search_fields = ['username','name']

    def call(self, obj):
        return mark_safe(f"<a href=\"tel:+{obj.phonenumber}\" target=\"_blank\">{obj.name}</a>")

    call.short_description = "qo'ng'iroq qilish"

    def telegram(self, obj):
        return mark_safe(f"<a href=\"https://t.me/{obj.username}\" target=\"_blank\">{obj.username}</a>")

    telegram.short_description = "telegram orqalik bog'lanish"

