from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Bucket, Task


class BucketModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.bucket = Bucket.objects.create(title='Test Bucket', description='Test Description', owner=self.user)

    def test_str_method(self):
        self.assertEqual(str(self.bucket), 'Test Bucket')

    def test_get_absolute_url(self):
        url = reverse('bucket-detail', kwargs={'pk': self.bucket.pk})
        self.assertEqual(self.bucket.get_absolute_url(), url)

    def test_tasks_completed_count(self):
        self.assertEqual(self.bucket.tasks_completed_count, 0)

        Task.objects.create(title='Test Task', bucket=self.bucket, complete=True)
        Task.objects.create(title='Test Task', bucket=self.bucket, complete=False)
        self.assertEqual(self.bucket.tasks_completed_count, 1)
        
        Task.objects.create(title='Test Task', bucket=self.bucket, complete=True)
        self.assertEqual(self.bucket.tasks_completed_count, 2)

    def test_all_tasks_completed(self):
        self.assertFalse(self.bucket.all_tasks_completed)
        
        task1 = Task.objects.create(title='Test Task', bucket=self.bucket, complete=False)
        task2 = Task.objects.create(title='Test Task', bucket=self.bucket, complete=False)
        self.assertFalse(self.bucket.all_tasks_completed)
        
        task1.complete = True
        task1.save()
        self.assertFalse(self.bucket.all_tasks_completed)
        
        task2.complete = True
        task2.save()
        self.assertTrue(self.bucket.all_tasks_completed)


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.bucket = Bucket.objects.create(title='Test Bucket', description='Test Description', owner=self.user)
        self.task = Task.objects.create(title='Test Task', description='Test Description', bucket=self.bucket)

    def test_str_method(self):
        self.assertEqual(str(self.task), 'Test Task')

    def test_get_absolute_url(self):
        url = reverse('bucket-detail', kwargs={'pk': self.bucket.pk})
        self.assertEqual(self.task.get_absolute_url(), url)

    def test_formatted_description(self):
        formatted_desc = self.task.formatted_description
        self.assertTrue('<p>Test Description</p>' in formatted_desc)