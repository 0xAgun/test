from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserCreationForm, Signupform, Reportform, ImageForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Lincesekeys, Userreports, UserProfile, Images, Comments
from django.contrib.auth.models import User
from .decorators import allowd_users
from notifications.signals import notify
import json


def home(request):
    # return HttpResponse("bla bla")
    return render(request, 'core/home1.html')

#user registration section // 

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST': #takes the post request
            form = Signupform(request.POST) #verifies the request
            if form.is_valid():
                form.save() # save it to database
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


#logout section

def request_logout(request):
    logout(request)
    return redirect('login')

#profile section

@login_required(login_url='login')
def profile(request):
    user_data = Userreports.objects.filter(admin_approved=True, user= request.user) #getting curent user all the reports
    approv = Userreports.objects.filter(user= request.user)
    sum = 0
    for x in user_data:
        sum += x.get_points()
    context = {"user_poiint": sum, "approves": approv}
    return render(request, 'core/profile.html', context)


#login section

def logins(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            lgusername = request.POST['username'] #username value from html form
            lgpassword = request.POST['password'] #password value from html form
            user = authenticate(username=lgusername, password=lgpassword) #checking for validation
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, "Invalid information. Try Again woth valid Credintials")
                return redirect('login')
    else:
        return redirect('profile')
    return render(request, 'core/login.html')

#report section

def report_system(request):
    if request.user.is_authenticated:
        form = Reportform()
        if request.method == 'POST':
            form = Reportform(request.POST)
            files = request.FILES.getlist('image') #takes a list of images 
            if form.is_valid():
                saveform = form.save(commit=False)
                saveform.user = request.user
                saveform.save() #saving form 
                print(files)
                for i in files:
                    Images.objects.create(reports=saveform, image=i) #image save to db
                messages.success(request, "successfully submitted report, now refresh the page" )
                return redirect('report')
        else:
            imageform = ImageForm()
    else:
        return redirect('login')

    context = {'form':form, 'imgform':imageform}
    return render(request, 'core/report.html', context)


# filtering approved reprots using user id
def test(id):
    approved_report = Userreports.objects.filter(user=id, admin_approved=True)
    return approved_report

def leaderboard(request):
    users = [user for user in User.objects.all()]
    reports = Userreports.objects.all()
    point_lists = {}
    sum = 0
    for user in users:
        ids = user.id
        returns_filters = test(ids)
        store = 0
        for x in returns_filters:
            store += x.get_points()
            point_lists[user.username] = store

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
    if request.method == 'POST':
        get_body = request.POST.get('comment_body')
        saving_comment = Comments.objects.create(reports=single ,body=get_body, user=request.user)
        recipient = User.objects.get(id=single.user.id) 
        notify.send(recipient, recipient=recipient, verb='Admin commented on your report', description=f"{single.title} check this for more info. ")

    show_reprot = Comments.objects.filter(reports=single)
    context = {
        'datas':single,
        'imagess':single_images,
        'comments': show_reprot,
    }
    return render(request, 'core/details_repo.html', context)


def error_page(request, exception):
    return render(request, 'core/404page.html')

def detail_view_user(request, pk):
    report = Userreports.objects.get(id = pk)
    single_images = Userreports.objects.get(id=pk).images_set.all()
    if request.user.id == report.user.id:
        if request.method == 'POST':
            get_body = request.POST.get('comment_body')
            saving_comment = Comments.objects.create(reports=report ,body=get_body, user=request.user)
    else:
        return HttpResponse("bade harami hoo")
        # saving_comment.save()

    show_reprot = Comments.objects.filter(reports=report)
    context = {
        'datas':report,
        'imagess':single_images,
        'comments': show_reprot,
    }
    # return render(request, 'core/users_report_details.html', context)
    return render(request, 'core/rest.html', context)

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