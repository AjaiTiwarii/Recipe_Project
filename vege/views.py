from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return HttpResponse("<h1>Home page of my recipe project</h1>")


@login_required(login_url="/login/")
def recipe(request):

    # data = request.POST # POST method se hum log data frontend se backend pr laate h
    # print(data)

    if request.method == "POST":

        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')

        Recipe.objects.create(
            recipe_image = recipe_image,
            recipe_name = recipe_name,
            recipe_description = recipe_description,
        )

        return redirect('/recipes/')  # this will remove " confirm form resubmission popup "
    
    queryset = Recipe.objects.all()

    # search ka logic
    if request.GET.get('search'):
        queryset = queryset.filter(recipe_name__icontains = request.GET.get('search'))



    context = {'recipes' : queryset}

        # print(recipe_name)
        # print(recipe_description)
        # print(recipe_image)

    return render(request, 'recipe.html', context)

@login_required(login_url="/login/")
def delete_recipe(request, id):

    query = Recipe.objects.get(id = id)
    query.delete()
    return redirect('/recipes/')


@login_required(login_url="/login/")
def update_recipe(request, id):
    query = Recipe.objects.get(id = id)

    if request.method == "POST":
        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')

        query.recipe_name = recipe_name
        query.recipe_description = recipe_description

        if recipe_image:
            query.recipe_image = recipe_image

        query.save()

        return redirect('/recipes/')


    context = {'update_recipes' : query}

    return render(request, 'update_recipes.html', context)


def login_page(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')
        
        user = authenticate(username = username, password = password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login/')
        
        else :
            login(request , user)
            return redirect('/recipes/')


    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('/login/')



def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check for existing username
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already taken')
            return render(request, 'register.html')

        # Create the user using create_user method which hashes the password
        user = User.objects.create_user(
            username=username,
            #password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save()

        messages.info(request, 'Account created Successfully')

        return redirect('/register/')

    return render(request, 'register.html')
