#mini_fb/urls.py
#created by Mike Greene

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView, UpdateStatusView # our view class definition 

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all'),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='profile'),
    path('profile/create_profile', CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update', UpdateStatusView.as_view(), name='update_status'),
]

