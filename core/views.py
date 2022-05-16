from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserCreationForm, Signupform, Reportform, ImageForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Lincesekeys, Userreports, UserProfile, Images
from django.contrib.auth.models import User
from .decorators import allowd_users
import json


def home(request):
    return HttpResponse("sdsdsd")

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = Signupform(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Registration successful. now go to Login Page" )
                return redirect('signup')
            else:
                messages.error(request, "Unsuccessful registration. Invalid information.")
        else:
            form = Signupform()
    else:
        return redirect('profile')  

    context = {"form": form}
    return render(request, 'core/signup.html', context)

def request_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    gg = Userreports.objects.filter(admin_approved=True, user= request.user)
    sum = 0
    for x in gg:
        sum += x.get_points()
    context = {"user_poiint": sum}
    return render(request, 'core/profile.html', context)

def logins(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            lgusername = request.POST['username']
            lgpassword = request.POST['password']
            user = authenticate(username=lgusername, password=lgpassword)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, "Invalid information. Try Again woth valid Credintials")
                return redirect('login')
    else:
        return redirect('profile')
    return render(request, 'core/login.html')


def report_system(request):
    if request.user.is_authenticated:
        form = Reportform()
        if request.method == 'POST':
            form = Reportform(request.POST)
            files = request.FILES.getlist('image')
            if form.is_valid():
                saveform = form.save(commit=False)
                saveform.user = request.user
                saveform.save()
                print(files)
                for i in files:
                    Images.objects.create(reports=saveform, image=i)
                # form.instance.user = request.user
                # form.save()
                messages.success(request, "successfully submitted report, now refresh the page" )
                return redirect('report')
        else:
            imageform = ImageForm()
    else:
        return redirect('login')

    context = {'form':form, 'imgform':imageform}
    return render(request, 'core/report.html', context)

def test(id):
    pp = Userreports.objects.filter(user=id, admin_approved=True)
    return pp

def leaderboard(request):
    users = [user for user in User.objects.all()]
    reports = Userreports.objects.all()
    point_lists = {}
    sum = 0
    for user in users:
        kk = user.id
        gr = test(kk)
        ggss = 0
        for x in gr:
            ggss += x.get_points()
            point_lists[user.username] = ggss

    ranks = {k: v for k, v in sorted(point_lists.items(), key=lambda item: item[1], reverse=True)}
    context = {
        'ranks' : ranks
    }
    return render(request, 'core/leaderboard.html', context)


@allowd_users(allowed_roles=['triage_team'])
def view_reports(request):
    all_repo = Userreports.objects.filter(admin_approved=False).order_by('-date_of_report')
    context = {
        'reports': all_repo
    }
    return render(request, 'core/reports_display.html', context)

@allowd_users(allowed_roles=['triage_team'])
def detail_view(request, pk):
    single = Userreports.objects.get(id = pk)
    single_images = Userreports.objects.get(id=pk).images_set.all()
    context = {
        'datas':single,
        'imagess':single_images,
    }
    return render(request, 'core/details_repo.html', context)


def error_page(request, exception):
    return render(request, 'core/404page.html')


def veri(request):
    if request.method == 'POST':
        allkeys = Lincesekeys.objects.all()
        key = request.POST['key']
        for cabi in allkeys:
            if cabi.Keys == key:
                msg = {'key_success':'valid key'}
                return HttpResponse(json.dumps(msg), content_type="application/json", status=200)
            else:
                msg = {'key_error':'not valid key'}
                return HttpResponse(json.dumps(msg), content_type="application/json", status=404)
        print(key)
    return render(request, 'core/verify.html')