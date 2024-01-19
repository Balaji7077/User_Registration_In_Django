from django.shortcuts import render

# Create your views here.
from app.forms import *

def registration(request):
    uf=UserForm()
    pf=ProfileForm()
    d={'uf':uf,'pf':pf}
    return render(request,'registration.html',d)