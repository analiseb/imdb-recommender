from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# from recommender import basic_recommender
from users.models import MoviesListUser


# Create your views here.
@login_required(login_url='/login')
def mymovies(request):

    if request.method == "POST":
        movies_delete = MoviesListUser.objects.filter(
            user=request.user,
            title=request.POST.get('title')
            )
        movies_delete[0].delete()
    my_movies = MoviesListUser.objects.filter(user=request.user)
    
    return render(
        request, 
        "users/my_movies.html",
            {
                'my_movies':my_movies,
            }
        )
    return render(request, "users/my_movies.html", {'saved_movies':saved_movies,})

def register(request):
    
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                do_login(request, user)
                return redirect('/welcome')

    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None
    return render(request, "users/register.html", {'form': form})


def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                do_login(request, user)
                return redirect('/mymovies')

    return render(request, "users/login.html", {'form': form})

def logout(request):
    do_logout(request)
    return redirect('/')
