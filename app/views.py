from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from app.forms import UserForm, ProfileForm
from app.models import Profile
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import random
from app.models import User
from app.utils import generate_otp
from django.contrib.auth.views import PasswordResetView

def registration(request):
    uf = UserForm()
    pf = ProfileForm()
    d = {'uf': uf, 'pf': pf}

    if request.method == 'POST' and request.FILES:
        uf = UserForm(request.POST)
        pf = ProfileForm(request.POST, request.FILES)

        if uf.is_valid() and pf.is_valid():
            MUFDO = uf.save(commit=False)
            pw = uf.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()

            MPFDO = pf.save(commit=False)
            MPFDO.username = MUFDO
            MPFDO.save()

            send_mail('registration',
                      'Thank You For Registration',
                      'lovies23july2023@gmail.com',
                      [MUFDO.email],
                      fail_silently=False,
                      )
            return HttpResponse('Registration data successfully')
        else:
            return HttpResponse('Invalid Data')
    return render(request, 'registration.html', d)

def home(request):
    if request.session.get('username'):
        username = request.session.get('username')
        d = {'username': username}
        return render(request, 'home.html', d)
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['un']
        password = request.POST['pw']
        AUO = authenticate(username=username, password=password)
        if AUO and AUO.is_active:
            login(request, AUO)
            request.session['username'] = username
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def profile_display(request):
    un = request.session.get('username')
    UO = User.objects.get(username=un)
    PO = Profile.objects.get(username=UO)
    d = {'UO': UO, 'PO': PO}
    return render(request, 'profile_display.html', d)

@login_required
def change_password(request):
    if request.method == 'POST':
        pw = request.POST['pw']
        rpw=request.POST['rpw']
        if pw==rpw:

            username = request.session.get('username')
            UO = User.objects.get(username=username)
            UO.set_password(pw)
            UO.save()

            send_mail('change_password',
                     'Your Password Has been Changed Successfully',
                    'lovies23july2023@gmail.com',
                    [UO.email],
                    fail_silently=False,
                     )
            return render(request,'user_login.html ')
    return render(request, 'change_password.html')

def reset_password(request):
    global user
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()

        if user:
            otp = generate_otp()

            request.session['reset_password_otp'] = otp
            print(f"OTP stored in session: {otp}")
            request.session['reset_password_username'] = username

            send_mail(
                'Password Reset OTP',
                f'Your OTP for password reset is: {otp}\n\nThis OTP is valid for a short duration.',
                'lovies23july2023@gmail.com',  
                [user.email],
                fail_silently=False,
            )

            return redirect('otp_p')
        else:
            return render(request, 'reset_password.html', {'error': 'User does not exist'})

    return render(request, 'reset_password.html', {'error': ''})

def otp_p(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('reset_password_otp')

        if entered_otp is not None:
            try:
                entered_otp_int = int(entered_otp)
                if stored_otp and entered_otp_int == stored_otp:
                    
                    return render(request, 'Reseet_password.html')
                else:
                    return render(request, 'otp.html', {'error': 'Invalid OTP'})
            except ValueError:
                return render(request, 'otp.html', {'error': 'Invalid OTP format'})
        else:
            return render(request, 'otp.html', {'error': 'OTP not provided'})

    return render(request, 'otp.html', {'error': ''})

def forget_password(request):
    if request.method == 'POST':
        pw = request.POST['pw']
        rpw=request.POST['rpw']
        
        if pw==rpw:

            user= request.session.get('username')
            user = User.objects.get(username=user)
            user.set_password(pw)
            user.save()

            send_mail('change_password',
                     'Your Password Has been Changed Successfully',
                    'lovies23july2023@gmail.com',
                    [user.email],
                    fail_silently=False,
                     )
            return render(request,'Reseet_password.html')
    return render (request,'forget_password.html')