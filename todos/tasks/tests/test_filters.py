from django.test import TestCase
from django.contrib.auth import get_user_model
from tasks.models import Task, TaskStatus
from tasks.filters import TaskFilter
from django.contrib.auth.models import User

class TaskFilterTests(TestCase):
    
    def setUp(self):
        """Set up a user and some tasks"""
        # Create a test user
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            username='test',
            password='aStrongPassword'
        )
        self.user.save()

        # Create tasks with different statuses
        Task.objects.create(
            title='Open Task 1',
            description='This is an open task',
            status=TaskStatus.OPEN,
            user=self.user
        )
        Task.objects.create(
            title='Completed Task 1',
            description='This is a completed task',
            status=TaskStatus.COMPLETED,
            user=self.user
        )
        Task.objects.create(
            title='Open Task 2',
            description='This is another open task',
            status=TaskStatus.OPEN,
            user=self.user
        )
        Task.objects.create(
            title='Completed Task 2',
            description='This is another completed task',
            status=TaskStatus.COMPLETED,
            user=self.user
        )

    def test_filter_by_title(self):
        """Test filtering tasks by title"""
        # Create the filter object with the query parameters
        filter = TaskFilter({'title': 'Open Task'}, queryset=Task.objects.all())

        # Filtered queryset should only contain tasks with 'Open Task' in the title
        filtered_tasks = filter.qs

        self.assertEqual(filtered_tasks.count(), 2)
        self.assertTrue(all('Open Task' in task.title for task in filtered_tasks))

    def test_filter_by_status(self):
        """Test filtering tasks by status"""
        # Test filter with completed=True (status=TaskStatus.COMPLETED)
        completed_filter = TaskFilter({'completed': True}, queryset=Task.objects.all())
        completed_tasks = completed_filter.qs
        self.assertEqual(completed_tasks.count(), 2)
        self.assertTrue(all(task.status == TaskStatus.COMPLETED for task in completed_tasks))

        # Test filter with completed=False (status=TaskStatus.OPEN or any other that might be added)
        open_filter = TaskFilter({'completed': False}, queryset=Task.objects.all())
        open_tasks = open_filter.qs
        self.assertEqual(open_tasks.count(), 2)
        self.assertTrue(all(task.status == TaskStatus.OPEN for task in open_tasks))

    def test_empty_filter(self):
        """Test that no filters return all tasks"""
        filter = TaskFilter({}, queryset=Task.objects.all())
        filtered_tasks = filter.qs
        self.assertEqual(filtered_tasks.count(), 4)  # Should return all tasks created in the setup
