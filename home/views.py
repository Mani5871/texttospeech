from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_view
from django.contrib.auth import logout
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
import pyttsx3
from .models import File
import os
from pathlib import Path
# Create your views here.


def words(request):
    if request.method == "POST":
        text = request.POST.get('text')
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        request.session['words'] = text
        return redirect('/')

def files(request):
    if request.method == "POST":
        file_content = request.FILES['file'].read()
        file_content = file_content.decode("utf-8", errors = "ignore")
        engine = pyttsx3.init()
        engine.say(file_content)
        engine.runAndWait()
        request.session['files'] = file_content
        
        file_name = request.FILES['file']
        user = User.objects.get(username=request.session['user'])
        author = user

        obj = File.objects.create(file_name = file_name, author = author)
        obj.save()
        return redirect('/')
    

def index(request):

    try:
        username = request.session['user']
        username = username + 'a'
    except:
        return redirect('signin/')

    try:
        
        user_objects = File.objects.filter(author_id__exact = request.session['id'])
        user_files = user_objects.values('file_name')
        file_list = []
        for items in user_files:
            file_list.append(items['file_name'])
        context = {'text': request.session['words'], 'user_files': file_list}
        del request.session['words']
        
        return render(request, 'index.html', context)
    
    except:
        pass
    
    try:
        if request.session['new_file'] != None:
            user_objects = File.objects.filter(author_id__exact = request.session['id'])
            user_files = user_objects.values('file_name')
            file_list = []
            for items in user_files:
                file_list.append(items['file_name'])
            context = {'text': request.session['new_file'], 'user_files': file_list}
            del request.session['new_file']
            return render(request, 'index.html', context)
    except:
        pass


    try:
        user_objects = File.objects.filter(author_id__exact = request.session['id'])
        user_files = user_objects.values('file_name')
        file_list = []
        for items in user_files:
            file_list.append(items['file_name'])
        context = {'text': request.session['files'], 'user_files': file_list}
        del request.session['files']
        return render(request, 'index.html', context)
    
    except:
        user_objects = File.objects.filter(author_id__exact = request.session['id'])
        user_files = user_objects.values('file_name')
        file_list = []
        for items in user_files:
            file_list.append(items['file_name'])
        return render(request, 'index.html', {'text': "Welcome {}".format(request.session['user']), 'user_files': file_list})

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)

        if user is not None:
            request.session['user'] = username
            request.session['id'] = request.user.id
            user_object = User.objects.get(username__exact = username)
            request.session['id'] = user_object.id
            return redirect('/')
        else:
            context = {'text':'Please check your credentials'}
            return render(request, 'signin.html', context)
    
    return render(request, 'signin.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        password_again = request.POST.get('password_again')

        if password == password_again:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                return render(request, 'signin.html')
            except:
                context = {'text': 'Username already existed. Please try again'}
                return render(request, 'signup.html', context)
        else:
            context = {'text': 'Password not matched'}
            return render(request, 'signup.html', context)

    return render(request, 'signup.html')


def signout(request):
    request.session['user'] = None
    request.session.flush()
    logout(request)
    return redirect('/signin')

def myfile(request):
    file_name = request.POST.get('file')
    cwd = Path.cwd()
    new_file = open(cwd/"media"/file_name, "r")
    file_content = new_file.read()
    engine = pyttsx3.init()
    engine.say(file_content)
    engine.runAndWait()

    request.session['new_file'] = file_content

    return redirect('/')