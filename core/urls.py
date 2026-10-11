from django.urls import path
from django.contrib.auth import views as auth_view
from . import views 
from .forms import LoginForm
app_name= "core"

urlpatterns=[
    path("",views.index,name="index"),
    path("contact/",views.contact,name="contact"),
    path("signup/",views.signup,name="signup"),
    path("login/",auth_view.LoginView.as_view(template_name="core/login.html" , authentication_form=LoginForm),name="login"),
    path("about/",views.about,name="about"),
    path("privacy/",views.privacy,name="privacy"),
    path("terms/",views.terms,name="terms"),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
