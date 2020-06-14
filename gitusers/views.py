from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def gitAuthView(request):
    return render(request, 'userTemplates/git-auth.html')

def loginRedirect(response):
    return redirect('/login/')
