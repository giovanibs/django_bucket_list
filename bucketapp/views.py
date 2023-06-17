from django.views.generic import (
    ListView, DetailView, UpdateView, CreateView, DeleteView
    )
from bucketapp.models import Bucket, Task
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# Create your views here.
def register(request):
    return render(
        request=request,
        template_name='bucket/register.html'
    )    
  
    
class TaskCreate(CreateView):
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
    
    
class BucketCreate(CreateView):
    model = Bucket
    
    # @todo: remove 'owner' field after adding user authentication 
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'create'
        return context
    

class BucketList(ListView):
    model = Bucket
    context_object_name = 'buckets'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BucketDetail(DetailView):
    model = Bucket
    context_object_name = 'bucket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bucket = self.get_object()  # Get the bucket instance
        context['ordered_task_list'] = bucket.tasks.all().order_by('complete')
        return context


class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'
    
    
class BucketUpdate(UpdateView):
    model = Bucket
    fields = '__all__'
    
    
class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('bucket-list')
    
    
class BucketDelete(DeleteView):
    model = Bucket
    success_url = reverse_lazy('bucket-list')
    
    
def task_complete(request, pk):
    task = get_object_or_404(Task, id=pk)
    task.complete = not task.complete
    task.save()
    return HttpResponseRedirect(reverse('bucket-detail', args=[task.bucket.pk]))