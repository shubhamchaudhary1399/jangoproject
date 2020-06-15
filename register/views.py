from django.shortcuts import render, redirect
from register.forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form  = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = RegisterForm()

    return render(request, 'register/register.html', {"form": form})
