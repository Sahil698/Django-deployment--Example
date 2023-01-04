from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileinfoform
from .models import UserProfileinfo
# Create your views here.

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate ,login , logout 


def pic(request):
    if request.method == "GET":
        pic_list= UserProfileinfo.objects.only('profile_pic')
    return render(request , 'basic_app/pic.html' , {'pic_list':pic_list})


def index(request):
    return render(request , 'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("You're logged in")



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered =  False

    if request.method == "POST":
        User_form  =  UserForm(data= request.POST)
        Profile_form = UserProfileinfoform(data  = request.POST)

        if User_form.is_valid() and Profile_form.is_valid():
            user =  User_form.save()
            user.set_password(user.password)
            user.save()

            profile =  Profile_form.save(commit=False)
            profile.user =  user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()

            registered = True
        else:
            print(User_form.errors ,  Profile_form.errors)
    else:
        User_form =  UserForm()
        Profile_form =  UserProfileinfoform()
    return render(request, 'basic_app/registration.html', {'User_form':User_form, 'Profile_form' : Profile_form , 'registered':registered})



def user_login(request):
 #user has filled out the form
    if request.method  == 'POST':
        username  = request.POST.get('username')
        password =  request.POST.get('password')

        user =  authenticate(username = username  ,password = password)

        if user:
            if user.is_active:
                login(request  , user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login an failed")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("Invalid credentials supplied")
    else:
        return render(request , 'basic_app/login.html')



    
    



        



