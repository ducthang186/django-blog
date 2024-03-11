from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('drafts/', views.draft_list, name='draft_list'),
    path('post/<int:pk>/publish/', views.publish_post, name='publish_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    # Additional URL patterns...
]
