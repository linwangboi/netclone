import json
import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Movie, MovieList

@login_required(login_url='login')
def index(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'index.html', context)

@login_required(login_url='login')
def movie(request, pk):
    movie = Movie.objects.get(uu_id=pk)
    context = {'movie': movie}
    return render(request, 'movie.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')   
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already used')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already used')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                auth.login(request, user)
                return redirect('/')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')
    return render(request, 'signup.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

def my_list(request):
    pass

@login_required(login_url='login')
def add_to_list(request):
    if request.method == 'POST':
        movie_url_id = request.POST.get('movie_id')
        uuid_pattern = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'
        movie_id = re.search(uuid_pattern, movie_url_id).group(0)
        
        movie = get_object_or_404(Movie, uu_id=movie_id)
        # Here you would add logic to add the movie to the user's list
        movie_list, created = MovieList.objects.get_or_create(owner_user=request.user, movie=movie)
        response_data = {'status': 'success', 'message': 'Added!'} if created else {'status': 'info', 'message': 'Movie already in your list.'}  
        return JsonResponse(response_data)
    else:
        response_data = {'status': 'error', 'message': 'Invalid request method.'}
        return JsonResponse(response_data, status=400)
        