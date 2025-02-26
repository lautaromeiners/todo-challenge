import django_filters
from tasks.models import Task, TaskStatus
from django.db.models import Q


class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr="icontains"
    )  # Case-insensitive partial match
    completed = django_filters.BooleanFilter(
        field_name="status", method="filter_completed"
    )

    class Meta:
        model = Task
        fields = ["title", "status"]

    def filter_completed(self, queryset, name, value):
        if value:
            return queryset.filter(status=TaskStatus.COMPLETED)
        return queryset.exclude(status=TaskStatus.COMPLETED)
