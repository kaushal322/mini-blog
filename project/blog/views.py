from django.shortcuts import render, redirect
from . forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from . import models
from django.contrib.auth.models import Group
# Create your views here.


def home(request):
    post = Post.objects.all()
    return render(request, "blog/home.html", {'posts': post})


def about(request):
    return render(request, "blog/about.html")


def contact(request):
    return render(request, "blog/contact.html")


def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, "blog/dashboard.html", {'posts': posts, 'full_name': full_name, 'groups': gps})
    else:
        return redirect("login")


def user_logout(request):
    logout(request)
    return redirect("home")


def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! You have become an Author.')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, "blog/signup.html", {'form': form})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully!!')
                    return redirect("dashboard")
        else:
            form = LoginForm()
        return render(request, "blog/login.html", {'form': form})
    else:
        return redirect('dashboard')


def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("dashboard")
        else:
            form = PostForm()
            return render(request, "blog/addpost.html", {'form': form})
    else:
        return redirect("login")

def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = Post.objects.get(id=id)
            form = PostForm(request.POST, instance=data)
            if form.is_valid():
                form.save()
        else:
            data = Post.objects.get(id=id)
            form = PostForm(instance=data)
            return render(request, "blog/updatepost.html", {'form': form})
    else:
        return redirect("login")

def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = Post.objects.get(id=id)
            data.delete()
        return redirect("dashboard")
    else:
        return redirect("login")

