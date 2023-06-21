from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from bucketapp.models import Bucket, Task
from bucketapp.views import TaskCreate, BucketCreate, BucketList, BucketDetail, TaskUpdate, \
    BucketUpdate, TaskDelete, BucketDelete, task_toggle_complete
from django.contrib.messages.middleware import MessageMiddleware


class ViewsTestCase(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.login(username='testuser', password='testpassword')
        
        self.bucket = Bucket.objects.create(title='Test Bucket', owner=self.user)
        self.other_bucket = Bucket.objects.create(title='Other Bucket', owner=self.other_user)
        
        self.task = Task.objects.create(title='Test Task', description='Test Description',
                                        bucket=self.bucket, assignee=self.user)
        
    def test_task_create_GET(self):
        url = reverse('task-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bucketapp/task_form.html')

    def test_task_create_POST(self):
        url = reverse('task-create')
        response = self.client.post(
            url,{
                'title': 'New task',
                'description': '' ,
                'bucket': self.bucket.id,
                'assignee': '' ,
                }
            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/bucket/{self.bucket.id}/')
    
    def test_task_create_POST_permission_denied(self):
        url = reverse('task-create')
        response = self.client.post(url, {
                                          'title': 'New task',
                                          'description': '' ,
                                          'bucket': self.other_bucket.id,
                                          'assignee': '' ,
                }
            )
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'bucketapp/task_form.html')

    def test_bucket_create_GET(self):
        url = reverse('bucket-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bucketapp/bucket_form.html')

    def test_bucket_create_POST(self):
        url = reverse('bucket-create')
        response = self.client.post(
            url,{
                'title': 'New bucket',
                'description': 'This is a bucket.' ,
                'owner': self.user.id,
                }
            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/bucket/{Bucket.objects.last().id}/')
    
    def test_bucket_create_POST_permission_denied(self):
        url = reverse('bucket-create')
        response = self.client.post(url,
            {
            'title': 'Bucket for someone else.',
            'description': 'This will not be my bucket.' ,
            'owner': self.other_user.id,
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'bucketapp/bucket_form.html')
    
    

        # request = self.factory.get(url)
        # request.user = self.user
        
        # response = TaskCreate.as_view()(request)
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'bucketapp/task_form.html')
        
        # # Test permission denied for non-owner user
        # request.user = self.other_user
        # response = TaskCreate.as_view()(request)
        # self.assertEqual(response.status_code, 403)
        
    def test_bucket_delete_view_GET(self):
        url = reverse('bucket-delete', args=[self.bucket.pk])
        response = self.client.get(url)
    
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('bucketapp/bucket_confirm_delete.html')
        
    def test_bucket_delete_GET_permission_denied(self):
        url = reverse('bucket-delete', args=[self.other_bucket.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('bucket-list'))
        
    def test_bucket_delete_view_POST(self):
        url = reverse('bucket-delete', args=[self.bucket.pk])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('bucket-list'))
    
    def test_bucket_delete_view_POST_permission_denied(self):
        url = reverse('bucket-delete', args=[self.other_bucket.pk])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('bucket-list'))
    
    # def test_bucket_create_view(self):
    #     url = reverse('bucket-create')
    #     request = self.factory.get(url)
    #     request.user = self.user
        
    #     response = BucketCreate.as_view()(request)
    #     self.assertEqual(response.status_code, 200)
        
    # def test_bucket_list_view(self):
    #     url = reverse('bucket-list')
    #     request = self.factory.get(url)
    #     request.user = self.user
        
    #     response = BucketList.as_view()(request)
    #     self.assertEqual(response.status_code, 200)
        
    # def test_bucket_detail_view(self):
    #     url = reverse('bucket-detail', args=[self.bucket.pk])
    #     request = self.factory.get(url)
    #     request.user = self.user
        
    #     response = BucketDetail.as_view()(request, pk=self.bucket.pk)
    #     self.assertEqual(response.status_code, 200)
        
    # def test_task_update_view(self):
    #     url = reverse('task-update', args=[self.task.pk])
    #     request = self.factory.get(url)
    #     request.user = self.user
        
    #     middleware = MessageMiddleware()
    #     middleware.process_request(request)

    #     response = TaskUpdate.as_view()(request, pk=self.task.pk)
    #     self.assertEqual(response.status_code, 200)
        
    #     # Test permission denied for non-owner user
    #     request.user = self.other_user
    #     response = TaskUpdate.as_view()(request, pk=self.task.pk)
    #     self.assertEqual(response.status_code, 403)
        
    # def test_bucket_update_view(self):
    #     url = reverse('bucket-update', args=[self.bucket.pk])
    #     request = self.factory.get(url)
    #     request.user = self.user
        
    #     response = BucketUpdate.as_view()(request, pk=self.bucket.pk)
    #     self.assertEqual(response.status_code, 200)
        
    #     # Test permission denied for non-owner user
    #     request.user = self.other_user
    #     response = BucketUpdate.as_view()(request, pk=self.bucket.pk)
    #     self.assertEqual(response.status_code, 403)
        
    # def test_task_delete_view(self):
    #     url = reverse('task-delete', args=[self.task.pk])
    #     request = self.factory.get(url)
    #     request.user = self.user
        
    #     response = TaskDelete.as_view()(request, pk=self.task.pk)
    #     self.assertEqual(response.status_code, 200)
        
    #     # Test permission denied for non-owner user
    #     request.user = self.other_user
    #     response = TaskDelete.as_view()(request, pk=self.task.pk)
    #     self.assertEqual(response.status_code, 403)
        
    # def test_bucket_delete_view(self):
    #     url = reverse('bucket-delete', args=[self.bucket.pk])
    #     request = self.factory.get(url)
    #     request.user = self.user
        
    #     response = BucketDelete.as_view()(request, pk=self.bucket.pk)
    #     self.assertEqual(response.status_code, 200)
        
    #     # Test permission denied for non-owner user
    #     request.user = self.other_user
    #     response = BucketDelete.as_view()(request, pk=self.bucket.pk)
    #     self.assertEqual(response.status_code, 403)
        
    # def test_task_toggle_complete_view(self):
    #     url = reverse('task-toggle-complete', args=[self.task.pk])
    #     request = self.factory.get(url)
    #     request.user = self.user
        
    #     response = task_toggle_complete(request, pk=self.task.pk)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, reverse('bucket-detail', args=[self.bucket.pk]))
        
    #     # Test permission denied for non-owner user or non-assignee user
    #     request.user = self.other_user
    #     response = task_toggle_complete(request, pk=self.task.pk)
    #     self.assertEqual(response.status_code, 403)