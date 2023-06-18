from django.urls import path
from bucketapp.views import (
    BucketList,
    BucketDetail,
    BucketUpdate,
    TaskUpdate,
    BucketCreate,
    TaskCreate,
    TaskDelete,
    BucketDelete,
    task_toggle_complete,
    )

urlpatterns = [
    path("", BucketList.as_view(), name="bucket-list"),
    path("home/", BucketList.as_view(), name="home"),
    
    # Bucket
    path("bucket/create/",          BucketCreate.as_view(), name="bucket-create"),
    path("bucket/<int:pk>/",        BucketDetail.as_view(), name="bucket-detail"),
    path("bucket/<int:pk>/update/",   BucketUpdate.as_view(), name="bucket-update"),
    path("bucket/<int:pk>/delete/",   BucketDelete.as_view(), name="bucket-delete"),
    
    # Task
    path("task/create/",    TaskCreate.as_view(), name="task-create"),
    path("task/<int:pk>/update/",  TaskUpdate.as_view(), name="task-update"),
    path("task/<int:pk>/toggle-complete/",  task_toggle_complete, name="task-toggle-complete"),
    path("task/<int:pk>/delete/",  TaskDelete.as_view(), name="task-delete"),
]