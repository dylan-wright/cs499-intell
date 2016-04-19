from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserCreationForm

# Create your views here.

def index(request):
    return render(request, "top_site/index.html")

@login_required
def profile(request):
    context = {"first_name": request.user}
    print (request.user)
    return render(request, "top_site/accounts/profile.html", context)

'''
    register

    http://www.djangobook.com/en/2.0/chapter14.html
'''
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/accounts/profile/")
    else:
        form = UserCreationForm()
    context = {'form':form}
    return render(request, "registration/register.html", context)
