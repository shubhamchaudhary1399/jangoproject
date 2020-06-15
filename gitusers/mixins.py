from django.contrib.auth.mixins import AccessMixin
from jangoproject.utils import get_or_none
from gitusers.models import GitHubAccountModel
from django.urls import reverse
from django.http import HttpResponseRedirect

class GitAuthRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        git_acc = get_or_none(GitHubAccountModel,user=request.user)
        if not git_acc or not git_acc.access_token:
            return HttpResponseRedirect(reverse('gitusers:git_auth'))
        return super().dispatch(request,*args,**kwargs)
