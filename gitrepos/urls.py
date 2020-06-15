
from django.urls import path
from gitrepos import views as repos_views


app_name = 'gitrepos'

urlpatterns = [
    path('create-hook/<repo>/', repos_views.CreateWebHook.as_view(), name='create_hook'),
    path('webhook/<repo>/', repos_views.HandleWebHook.as_view(), name='webhook_end'),
    path('list-selected/',repos_views.ListMyRepos.as_view(),name='list_selected_repos'),
    path('list-events/<repo>/',repos_views.ListAllEvents.as_view(),name='list_events')
]
