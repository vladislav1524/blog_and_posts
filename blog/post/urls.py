from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<str:username>/posts/', views.post_list, name='user_posts'),
    path('profile/<str:username>/', views.profile_info, name='profile_info'),
    path('post/<int:post_id>/', views.post_detail, name='detail'),
    path('post/create/', views.post_add, name='post_form'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/comment/', views.comment_add, name='comment_form'),
    path('post/comment/<int:comment_id>/edit/', views.comment_edit, name='comment_edit'),
    path('post/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
]
