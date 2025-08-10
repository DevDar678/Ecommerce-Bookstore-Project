
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.contrib.auth import logout


class SignUpView(generic.CreateView):
     form_class    = UserCreationForm
     success_url   = reverse_lazy('login')
     template_name = 'signup.html'
 
def logout_user(request):
     logout(request)
     return redirect('list')



