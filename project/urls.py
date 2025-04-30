from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
#Created by Mike Greene

''' URL patterns for the app'''
urlpatterns = [
    # map the URL (empty string) to the view
	path(r'', views.ShowAllProfilesView.as_view(), name='home'),
    path(r'show_all', views.ShowAllProfilesView.as_view(), name='show_all'),
    path('profile/create', views.CreateProfileView.as_view(), name='create'),
    path('profile/<int:pk>', views.ShowProfilePageView.as_view(), name='profile'),
    path('profile/<int:pk>/edit_review/<int:review_pk>', views.EditReivewView.as_view(), name='edit_review'),
    path('profile/<int:pk>/delete_review/<int:review_pk>', views.DeleteReviewView.as_view(), name='delete_review'),
    path('profile/<int:pk>/delete_videogamelist/<int:list_pk>', views.DeleteVideoGameListView.as_view(), name='delete_videogamelist'),
    path('profile/<int:profile_pk>/game/<int:game_pk>/add_review', views.CreateReviewView.as_view(), name='add_review'),
    path('profile/<int:profile_pk>/select_add_friend', views.SelectProfileToAdd.as_view(), name='select_add_friend'),
    path('profile/<int:profile_pk>/select_add_friend/<int:friend_pk>', views.AddFriendView.as_view(), name='added_friend'),
    path('profile/<int:profile_pk>/select_add_favorite', views.SelectVideoGameToAdd.as_view(), name='select_add_game'),
    path('profile/<int:profile_pk>/select_add_favorite/<int:game_pk>', views.AddFavoriteGameView.as_view(), name='add_game'),
    path('profile/<int:profile_pk>/videogamelists', views.VideoGameListsView.as_view(), name='videogame_lists'),
    path('profile/<int:profile_pk>/videogamelists/create', views.CreateVideoGameList.as_view(), name='create_videogamelist'),
    path('profile/create_profile', views.CreateProfileView.as_view(), name='create_profile'),
    path(r'show_all_videogames', views.ShowAllVideoGames.as_view(), name='show_all_videogames'),
    path('videogame/<int:pk>', views.ShowVideoGamePageView.as_view(), name='videogame'),
    path('reviews', views.ShowAllReviews.as_view(), name='reviews'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='project/logout.html'), name='logout'),
]