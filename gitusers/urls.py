from django.urls import path, include
from django.contrib.auth import views as auth_views
from gitusers import views as user_views

app_name = 'gitusers'

urlpatterns = [
    path('git-auth/', user_views.GitAuthView.as_view(), name='git_auth'),
    path('git-auth/verify/', user_views.GitAuthVerify.as_view(), name='git_auth_verify'),
    path('list-public-repo/', user_views.ListMyReposView.as_view(), name='home'),
]
