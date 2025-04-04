from django.urls import path
from . import views 

urlpatterns = [
    # map the URL (empty string) to the view
	path(r'', views.VotersListView.as_view(), name='home'),
    path(r'voters', views.VotersListView.as_view(), name='voters_list'),
    path(r'voters/<int:pk>', views.VoterDetailView.as_view(), name='voter_detail'),
    path(r'graphs', views.GraphsListView.as_view(), name='graphs'),
    
    
]