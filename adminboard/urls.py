from django.urls import path, include
from . import views

app_name= 'adminboard'
urlpatterns = [
    path('', views.loginadmin, name='loginadmin'),
    path('loginadminuser/', views.loginadminuser, name='loginadminuser'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('logout_admin/', views.logout_admin, name='logout_admin'),
    path('savemodule/', views.savemodule, name='savemodule'),
    path('visitmodule/<str:modname>/', views.visitmodule, name='visitmodule'),
    path('createcourse/', views.createcourse, name='createcourse'),
    path('addmodule/', views.addmodule, name='addmodule'),
    path('viewmodule/', views.viewmodule, name='viewmodule'),
    path('visitcourse/<str:cname>/', views.visitcourse, name='visitcourse'),
    path('savecourse/', views.savecourse, name='savecourse'),
    path('editcourse/<str:cname>/', views.editcourse, name='editcourse'),
    path('updatecourse/', views.updatecourse, name='updatecourse'),
    path('casestudy/', views.casestudy, name='casestudy'),
    path('finalquest/', views.finalquest, name='finalquest'),
    path('postscenario/', views.postscenario, name='postscenario'),
    path('assign/', views.assign, name='assign'),
    path('people/', views.people, name='people'),
    path('postquest/', views.postquest, name='postquest'),
    path('postassign/', views.postassign, name='postassign'),
    path('delmod/<str:modname>/', views.delmod, name='delmod'),
    path('delcourse/<str:cname>/', views.delcourse, name='delcourse'),
    path('putexpdate/<int:id>/', views.putexpdate, name='putexpdate'),
    path('testrestart/<int:id>/', views.testrestart, name='testrestart'),
    path('getcasestudy/', views.getcasestudy, name='getcasestudy'),
    path('getallquest/', views.getallquest, name='getallquest'),
    path('filterpeople/', views.filterpeople, name='filterpeople'),
    path('delprocess_name/<int:id>/', views.delprocess_name, name='delprocess_name'),
    path('addprocess_name/', views.addprocess_name, name='addprocess_name'),
    path('edit_quest/<int:id>/', views.edit_quest, name='edit_quest'),
    path('edit_scenario/<int:id>/', views.edit_scenario, name='edit_scenario'),
    path('revoke/<int:id>/', views.revoke, name='revoke'),
    path('upload_bulk_quest/', views.upload_bulk_quest, name='upload_bulk_quest'),
    path('editmod/<str:mname>/', views.editmod, name='editmod'),
    path('submission/', views.submission, name='submission'),
    path('status/<int:id>', views.status, name='status'),
    path('configuration/', views.configuration, name='configuration'),
    path('delCarousel/<id>/', views.delCarousel, name='delCarousel'),
    path('minMax/', views.minMax, name='minMax'),
    path('userassessment/', views.userassessment, name='userassessment'),
    path('questions/', views.questions, name='questions'),
    path('questionsForm/<int:id>', views.questionsForm, name='questionsForm'),
]
