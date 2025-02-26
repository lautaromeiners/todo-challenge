from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from tasks.models import Task, TaskStatus
from rest_framework.authtoken.models import Token


class TaskViewSetTestCase(APITestCase):

    def setUp(self):
        """
        Setup the test environment.
        """
        # Create a test user
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            username='test',
            password='aStrongPassword'
        )
        self.user.save()
        # Generate token for the user
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create some tasks for the user
        self.task1 = Task.objects.create(
            user=self.user,
            title="Test Task 1",
            description="Description for Task 1",
        )
        
        self.task2 = Task.objects.create(
            user=self.user,
            title="Test Task 2",
            description="Description for Task 2",
        )

        self.task3 = Task.objects.create(
            user=self.user,
            title="Completed Task",
            description="A completed task",
            status=TaskStatus.COMPLETED,
        )

    def test_list_tasks(self):
        """Test listing the tasks for the authenticated user"""
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_task(self):
        """Test creating a task"""
        url = reverse('task-list')
        data = {
            "title": "New Task",
            "description": "Description of new task",
            "status": TaskStatus.OPEN
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])

    def test_update_task_status(self):
        """Test marking a task as completed"""
        url = reverse('task-detail', kwargs={'pk': self.task1.id})
        data = {"status": TaskStatus.COMPLETED}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.status, TaskStatus.COMPLETED)

    def test_delete_task(self):
        """Test deleting a task"""
        url = reverse('task-detail', kwargs={'pk': self.task2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task2.id).exists())

    def test_unauthenticated_user(self):
        """Test that an unauthenticated user cannot access the tasks"""
        self.client.credentials()  # Remove authentication token
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_task_belonging_to_user(self):
        """Test that a user can only access their own tasks"""
        another_user = get_user_model().objects.create_user(email="other@example.com", username="anotheruser", password="anotherpassword")
        another_user.save()
        task_for_another_user = Task.objects.create(user=another_user, title="Another Task", description="A task for another user")
        
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(task_for_another_user.id, [task['id'] for task in response.data])
        self.assertEqual(len(response.data), 3) # Same three tasks as before, no new task

    def test_filter_by_title(self):
        """Test filtering tasks by title"""
        url = reverse('task-list') + '?title=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The response should only include the tasks with "Test" in their title
        self.assertEqual(len(response.data), 2)

    def test_filter_by_status_completed(self):
        """Test filtering tasks by completed status"""
        url = reverse('task-list') + '?completed=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The response should only include tasks that are marked as completed
        self.assertEqual(len(response.data), 1)
        self.assertTrue(all(task['status'] == TaskStatus.COMPLETED for task in response.data))

    def test_filter_by_status_open(self):
        """Test filtering tasks by open (not completed) status"""
        url = reverse('task-list') + '?completed=false'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The response should only include tasks that are not completed
        self.assertEqual(len(response.data), 2)
        self.assertTrue(all(task['status'] == TaskStatus.OPEN for task in response.data))

