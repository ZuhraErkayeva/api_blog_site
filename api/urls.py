from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('posts/<int:pk>/', views.post_detail, name='post-detail'),
    path('profiles/<int:pk>/', views.profile_detail, name='profile-detail'),
    path('posts/<int:pk>/like/', views.like_post, name='like-post'),
    path('users/<int:pk>/follow/', views.follow_user, name='follow-user'),
]
