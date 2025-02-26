from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from tasks.models import Task
from tasks.serializers import TaskSerializer
from tasks.filters import TaskFilter


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def perform_create(self, serializer):
        # Automatically assign the logged-in user to the task
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Only tasks belonging to the authenticated user are shown.
        """
        user = self.request.user
        return Task.objects.filter(user=user)
