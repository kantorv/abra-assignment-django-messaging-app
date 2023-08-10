from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["id","created","sender","receiver","subject","hide_for_receiver", "hide_for_sender"]
