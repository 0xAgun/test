from django.contrib import admin
from django.urls import path
from . import views

#django header customization

admin.site.site_header = "Bug Bounty Community BD"
admin.site.site_title = "wellcome to BBCBD Admin Panel"
admin.site.index_title = "Control server"

urlpatterns = [
    path('', views.home, name="home"),
    path('sign-up/', views.signup, name="signup"),
    path('logout/', views.request_logout, name="logout"),
    path('login/', views.logins, name="login"),
    path('profile/', views.profile, name="profile"),
    path('report/', views.report_system, name="report"),
    path('leaderboard/', views.leaderboard, name="leaderboard"),
    path('view_reports/', views.view_reports, name="view_reports"),
    path('view_reports/<int:pk>', views.detail_view, name="detail_reports"),
    path('validate/', views.veri, name="val"),

]
