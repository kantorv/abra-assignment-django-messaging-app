from django.shortcuts import render
from .models import Message
from core.models import User
from .serializers import MessageSerializer
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404
from django.db.models import Q

# Create your views here.

class MessageViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Message.objects.none()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get('pk')
        user= self.request.user

        # viewing particular message is allowed (just) to sender or receiver
        q1 = Q(sender=user, hide_for_sender=False)
        q2 = Q(receiver=user, hide_for_receiver=False)

        try:
            object =  Message.objects.get(q1|q2, pk=pk)
        except Message.DoesNotExist:
            raise Http404

        return object

    def create(self, request, *args, **kwargs):
        payload = request.data
        sender = self.request.user
        receiver_username = payload.get('to')
        subject = payload.get('subject')
        message = payload.get('message')

        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            response = {
                "error" : True,
                "code" : 1004,
                "message" : "Recipient does not exists"
            }
            return Response(response, status=status.HTTP_201_CREATED )



        data = dict(
            sender = sender.pk,
            receiver = receiver.pk,
            subject = subject,
            message = message
        )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer):
    #     serializer.save(sender=self.request.user)

    @action(detail=False)
    def sent(self, request, *args, **kwargs):
        queryset = Message.objects.filter(sender=request.user, hide_for_sender=False)
        #queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def received(self, request, *args, **kwargs):
        queryset = Message.objects.filter(receiver=request.user, hide_for_receiver=False)
        #queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=["DELETE"])
    def delete_recieved(self, request, *args, **kwargs):
        msg_ids = request.data
        objects = Message.objects.filter(receiver=self.request.user, hide_for_receiver=False, pk__in=msg_ids)
        cnt = objects.count()

        # TODO: handle msg_ids count not equal to fetched objects

        hide_list = objects.filter(hide_for_sender=False)
        hide_list.update(hide_for_receiver=True)

        #cleanup
        permanent_delete_list = objects.filter(hide_for_sender=True)
        permanent_delete_list.delete()

        return Response( status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["DELETE"])
    def delete_sent(self, request, *args, **kwargs):
        msg_ids = request.data
        objects = Message.objects.filter(sender=self.request.user, hide_for_sender=False, pk__in=msg_ids)
        cnt = objects.count()

        hide_list = objects.filter(hide_for_receiver=False)
        hide_list.update(hide_for_sender=True)

        # cleanup
        permanent_delete_list = objects.filter(hide_for_receiver=True)
        permanent_delete_list.delete()



        return Response(status=status.HTTP_204_NO_CONTENT)