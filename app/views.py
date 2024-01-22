from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from app.forms import *
from app.models import *
from django.core.mail import send_mail
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