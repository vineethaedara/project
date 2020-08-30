from django.urls import path

from . import views

app_name = 'vs'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path("login/",views.loginView,name='login'),
    path("logout/",views.logoutview,name='logout'),
    path("register/",views.registrationview,name='register'),
    path("poll/",views.pollview,name='poll'),
]   