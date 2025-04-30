from django.contrib import admin

# Register your models here.

from .models import Profile, VideoGame, Friend, Review, VideoGameList, FavoriteVideoGame
admin.site.register(Profile)
admin.site.register(VideoGame)
admin.site.register(Friend)
admin.site.register(Review)
admin.site.register(VideoGameList)
admin.site.register(FavoriteVideoGame)


