from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from jangoproject.utils import get_state_string
from gitusers.models import GitHubAccountModel
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponseRedirect
from django.views.generic.base import RedirectView
from gitusers.mixins import GitAuthRequiredMixin
from django.contrib import messages
import requests
import urllib

# @login_required(login_url='/login/')
# def gitAuthView(request):
#     return render(request, 'userTemplates/git-auth.html')

def loginRedirect(response):
    return redirect('/login/')

class ListMyReposView(LoginRequiredMixin,GitAuthRequiredMixin,generic.TemplateView):
    template_name = 'userTemplates/list-repos.html'
    def get_context_data(self,*args,**kwargs):
        context = super(ListMyReposView,self).get_context_data(*args,**kwargs)
        git_acc = self.request.user.github_acc
        r = requests.get('https://api.github.com/users/'+git_acc.git_username+'/repos',
                    headers={'Accept':'application/json'})
        context['repo_list'] = [[repo.get('name'),repo.get('description'),repo.get('id')] for repo in r.json()]
        return context


class GitAuthView(LoginRequiredMixin,generic.TemplateView):
    template_name = 'userTemplates/git-auth.html'
    def get_context_data(self,*args,**kwargs):
        context = super(GitAuthView,self).get_context_data(*args,**kwargs)
        git_acc, _ = GitHubAccountModel.objects.get_or_create(user=self.request.user)
        git_acc.state = get_state_string()
        git_acc.save()
        a = (('client_id','07708964cec37e18bed5'),
            ('redirect_uri','https://jangoproject-production.herokuapp.com/gitusers/git-auth/verify/'),
            ('login',self.request.user.username),('scope','repo'),
            ('state', git_acc.state))
        context['redirect_url'] = urllib.parse.urlencode(a)
        return context

class GitAuthVerify(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        git_acc = get_object_or_404(GitHubAccountModel,user=self.request.user)
        if not git_acc.state==self.request.GET.get('state'):
            return self.handel_failure()
        data = {
                'client_id': '07708964cec37e18bed5',
                'client_secret': 'a5d1d09e36af8048d2378fb2eedd058498fcb796',
                'code': self.request.GET.get('code'),
                'redirect_uri':'https://jangoproject-production.herokuapp.com/gitusers/git-auth/verify/',
                'state':git_acc.state
            }
        r = requests.post('https://github.com/login/oauth/access_token', data=data, headers={'Accept':'application/json'})
        result = r.json()
        print(result)
        if not result.get('access_token'):
            return self.handel_failure()
        git_acc.access_token = result.get('access_token')
        r1 = requests.get('https://api.github.com/user',headers={'Authorization':'token '+git_acc.access_token,
                            'Accept':'application/json'})
        result1 = r1.json()
        git_acc.git_username = result1.get('login')
        git_acc.save()
        return reverse('gitusers:home')
    def handel_failure(self):
        messages.error(self.request, 'Something went wrong, please try again.')
        return reverse('gitusers:git_auth')
