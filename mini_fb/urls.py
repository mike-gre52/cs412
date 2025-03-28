#mini_fb/urls.py
#created by Mike Greene

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView, UpdateStatusView, AddFriendView, ShowFriendSuggestionsView, ShowNewsFeedView # our view class definition 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all'),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='profile'),
    path('profile/create_profile', CreateProfileView.as_view(), name='create_profile'),
    path('status/create_status', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update', UpdateStatusView.as_view(), name='update_status'),
    path('profile/add_friend/<int:other_pk>', AddFriendView.as_view(), name='add_friend'),
    path('profile/friend_suggestions', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/news_feed', ShowNewsFeedView.as_view(), name='news_feed'),
    #Auth URLs
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'), ## NEW
	path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'), ## NEW
    #path('register/', RegistrationView.as_view(), name='register'),
]

