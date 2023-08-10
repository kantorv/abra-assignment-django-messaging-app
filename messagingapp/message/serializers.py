from rest_framework import serializers
from .models import Message
from core.models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#       model = User
#       fields = [ 'username']

class MessageSerializer(serializers.ModelSerializer):

    # changing representation for replacing sender and receiver id's with username field
    def to_representation(self, instance):
        representation = dict()
        representation["id"] = instance.id
        representation["subject"] = instance.subject
        representation["message"] = instance.message
        representation["created"] = instance.created
        representation["from"] = instance.sender.username
        representation["to"] = instance.receiver.username

        return representation

    class Meta:
        model = Message
        fields = ['id','created','subject', 'message','sender','receiver']