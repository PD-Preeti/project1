from django.urls import path
from . import views

app_name = 'employee'
urlpatterns = [
    path('', views.employeelogin, name='employeelogin'),
    path('home/', views.employeehome, name='employeehome'),
    path('your_courses/', views.your_courses, name='your_courses'),
    path('logout_emp/', views.logout_emp, name='logout_emp'),
    path('continuecourse/<str:cname>/', views.continuecourse, name='continuecourse'),
    path('coursestarted/<str:cname>/', views.coursestarted, name='coursestarted'),
    path('courseprogress/<str:cname>/<str:mname>/', views.courseprogress, name='courseprogress'),
    path('finalquest/<str:cname>/', views.finalquest, name='finalquest'),
    path('scorecal/', views.scorecal, name='scorecal'),
    path('postscenario/', views.postscenario, name='postscenario'),
    path('getrating/<str:empemail>/<str:cname>/', views.getrating, name='getrating'),
    path('postrating/<str:empemail>/<str:cname>/', views.postrating, name='postrating'),
    path('recommendations/', views.viewrecommendation, name='viewrecommendation'),
    path('acceptrecommendation/<str:cname>/<int:id>/', views.acceptrecommendation, name='acceptrecommendation'),
    path('rejectrecommendation/<int:id>/', views.rejectrecommendation, name='rejectrecommendation'),
    path('issueaction/', views.issueaction, name='issueaction'),
    path('your_contribution/', views.your_contribution, name='your_contribution'),
    path('contribute/', views.contribute, name='contribute'),
    path('dashboard/', views.dashboard, name='dashboard'),
]