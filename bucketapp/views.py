from django.views.generic import (
    ListView, DetailView, UpdateView, CreateView, DeleteView
    )
from bucketapp.models import Bucket, Task
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = [
        'title',
        'description',
        'bucket',
        'assignee',
    ]
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'create'
        return context
    
    
class BucketCreate(LoginRequiredMixin, CreateView):
    model = Bucket
    
    # @todo: remove 'owner' field after adding user authentication 
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'create'
        return context
    

class BucketList(LoginRequiredMixin, ListView):
    model = Bucket
    context_object_name = 'buckets'
    
    
    def get_queryset(self):
        request_user = self.request.user
        return Bucket.objects.filter(owner=request_user)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BucketDetail(LoginRequiredMixin, DetailView):
    model = Bucket
    context_object_name = 'bucket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bucket = self.get_object()  # Get the bucket instance
        context['ordered_task_list'] = bucket.tasks.all().order_by('complete')
        return context


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    
    
class BucketUpdate(LoginRequiredMixin, UpdateView):
    model = Bucket
    fields = '__all__'
    
    
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('bucket-list')
    
    
class BucketDelete(LoginRequiredMixin, DeleteView):
    model = Bucket
    success_url = reverse_lazy('bucket-list')
    

@login_required 
def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, id=pk)
    task.complete = not task.complete
    task.save()
    return HttpResponseRedirect(reverse('bucket-detail', args=[task.bucket.pk]))