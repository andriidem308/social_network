"""Landing urls."""
from django.urls import path, re_path

from .views import AddLike, last_activity, likes_analytics, PostListView

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('post/<int:pk>/like', AddLike.as_view(), name='like'),
    path('api/analytics/', likes_analytics, name='likes_analytics'),
    re_path(r'^api/lastactivity/(?P<username>\w+)/$', last_activity, name='last_activity')
]
