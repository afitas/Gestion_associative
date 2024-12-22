from django.urls import path
from . import views

urlpatterns = [
    path('', views.announcement_list, name='announcement-list'),
    path('create/', views.AnnouncementCreateView.as_view(), name='announcement-create'),
    path('<int:pk>/', views.announcement_detail, name='announcement-detail'),
    path('<int:pk>/update/', views.AnnouncementUpdateView.as_view(), name='announcement-update'),
    path('<int:pk>/delete/', views.AnnouncementDeleteView.as_view(), name='announcement-delete'),
]
