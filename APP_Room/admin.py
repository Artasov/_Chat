from django.contrib import admin
from django.contrib.admin import display

from .models import *


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['room_name', 'user', 'content', 'date_added']

    @display()
    def room_name(self, obj):
        return obj.room.name


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']