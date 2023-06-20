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
    template_name = 'bucketapp/task_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'create'
        return context
    
    
    def form_valid(self, form):
        bucket = form.cleaned_data['bucket']
        
        if self.request.user != bucket.owner:
            messages.error(self.request,
                       "You are not the owner of this bucket.",
                       # bootstrap tags
                       extra_tags="alert alert-warning alert-dismissible fade show"
        )
            return render(
                self.request,
                self.template_name,
                self.get_context_data(form=form),
                status=403
            )
        
        return super().form_valid(form)
    
    
class BucketCreate(LoginRequiredMixin, CreateView):
    model = Bucket
    fields = '__all__'
    template_name = 'bucketapp/bucket_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'create'
        return context
    
    def form_valid(self, form):
        owner = form.cleaned_data['owner']
        
        if self.request.user != owner:
            messages.error(self.request,
                       "You cannot create a bucket for another user.",
                       # bootstrap tags
                       extra_tags="alert alert-warning alert-dismissible fade show"
        )
            return render(
                self.request,
                self.template_name,
                self.get_context_data(form=form),
                status=403
            )
        
        return super().form_valid(form)
    

class BucketList(LoginRequiredMixin, ListView):
    model = Bucket
    context_object_name = 'buckets'
    
    
    def get_queryset(self):
        request_user = self.request.user
        return Bucket.objects.filter(owner=request_user)


class BucketDetail(LoginRequiredMixin, DetailView):
    model = Bucket
    context_object_name = 'bucket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bucket = self.get_object()
        context['ordered_task_list'] = bucket.tasks.all().order_by('complete')
        return context


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.request.user != self.object.bucket.owner:
            messages.error(self.request,
                       "You are not the owner of this bucket.",
                       # bootstrap tags
                       extra_tags="alert alert-warning alert-dismissible fade show"
            )
            referring_page = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(referring_page or reverse('bucket-list'))

        return super().dispatch(request, *args, **kwargs)
    
    
class BucketUpdate(LoginRequiredMixin, UpdateView):
    model = Bucket
    fields = '__all__'
    
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.request.user != self.object.owner:
            messages.error(self.request,
                       "You are not the owner of this bucket.",
                       # bootstrap tags
                       extra_tags="alert alert-warning alert-dismissible fade show"
        )
            referring_page = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(referring_page or reverse('bucket-list'))

        return super().dispatch(request, *args, **kwargs)

    
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('bucket-list')
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.request.user != self.object.bucket.owner:
            messages.error(self.request,
                       "You are not the owner of this bucket.",
                       # bootstrap tags
                       extra_tags="alert alert-danger alert-dismissible fade show"
        )
            referring_page = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(referring_page or reverse('bucket-list'))

        return super().dispatch(request, *args, **kwargs)
    
    
class BucketDelete(LoginRequiredMixin, DeleteView):
    model = Bucket
    success_url = reverse_lazy('bucket-list')
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.request.user != self.object.owner:
            messages.error(self.request,
                       "You are not the owner of this bucket.",
                       # bootstrap tags
                       extra_tags="alert alert-danger alert-dismissible fade show"
        )
            referring_page = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(referring_page or reverse('bucket-list'))

        return super().dispatch(request, *args, **kwargs)
    

@login_required 
def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, id=pk)
    
    if request.user in [task.assignee, task.bucket.owner]:
        task.complete = not task.complete
        task.save()
    else:
        messages.error(request,
                       "You are not the owner of the bucket or the task's assignee.",
                       # bootstrap tags
                       extra_tags="alert alert-warning alert-dismissible fade show"
        )
    return HttpResponseRedirect(reverse('bucket-detail', args=[task.bucket.pk]))