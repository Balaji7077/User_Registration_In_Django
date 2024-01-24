from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from app.forms import *
from app.models import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def registration(request):
    uf=UserForm()
    pf=ProfileForm()
    d={'uf':uf,'pf':pf}

    if request.method == 'POST' and request.FILES:
        uf=UserForm(request.POST)
        pf=ProfileForm(request.POST,request.FILES)

        if uf.is_valid() and pf.is_valid():
            MUFDO=uf.save(commit=False)
            pw=uf.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()

            MPFDO=pf.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()

            send_mail('registration',
                      'Thank You For Registration',
                      'lovies23july2023@gmail.com',
                      [MUFDO.email],
                      fail_silently=False,
                      )
            return HttpResponse('Registration data succsessfully')
        else:
            return HttpResponse('Invalid Data')
    return render(request,'registration.html',d)

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def user_login(request):
    if request.method == 'POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
    return render(request,'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
@login_required
def profile_display(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'profile_display.html',d)