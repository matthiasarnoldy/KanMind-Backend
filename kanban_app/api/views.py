from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import generics, permissions

from kanban_app.models import Board, Task, Comment
from kanban_app.api.serializers import BoardSerializer, BoardDetailSerializer, BoardPatchResponseSerializer, TaskSerializer, CommentSerializer
from kanban_app.api.permissions import IsBoardMemberOrOwner

class BoardListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardSerializer

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsBoardMemberOrOwner]
    lookup_url_kwarg = "board_id"

    def get_queryset(self):
        user = self.request.user
        return Board.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ("PATCH", "PUT"):
            return BoardPatchResponseSerializer
        return BoardDetailSerializer