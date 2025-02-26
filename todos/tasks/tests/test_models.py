from django.test import TestCase
from django.contrib.auth import get_user_model
from tasks.models import Task, TaskStatus

class TestTask(TestCase):

    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            username='test',
            password='aStrongPassword'
        )
        self.user.save()

    def test_task_creation(self):
        """Test that a task is created & user is set"""
        task = Task.objects.create(
            title='Test Task',
            description='This is a task description',
            status=TaskStatus.OPEN,
            user=self.user
        )
        
        # Verify the task is created and the user is associated correctly
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'This is a task description')
        self.assertEqual(task.status, TaskStatus.OPEN)
        self.assertEqual(task.user, self.user)

    def test_task_status_choices(self):
        """Test that task status choices are correct"""
        task_open = Task.objects.create(
            title='Open Task',
            description='This is an open task',
            status=TaskStatus.OPEN,
            user=self.user
        )
        task_completed = Task.objects.create(
            title='Completed Task',
            description='This is a completed task',
            status=TaskStatus.COMPLETED,
            user=self.user
        )

        # Verify the task status values
        self.assertEqual(task_open.status, TaskStatus.OPEN)
        self.assertEqual(task_completed.status, TaskStatus.COMPLETED)

    def test_task_str_method(self):
        """Test the string representation of the task"""
        task = Task.objects.create(
            title='Test Task',
            description='This is a task description',
            status=TaskStatus.OPEN,
            user=self.user
        )

        self.assertEqual(str(task), 'Test Task')