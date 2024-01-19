from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib.auth import logout
from django.core.mail import send_mail
from fainalproject import settings
import random
import requests
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    msg=""
    user=request.session.get('user')
    if request.method=='POST': #root
        if request.POST.get('signup')=='signup': #signup
            newuser=signupdata(request.POST)
            if newuser.is_valid():
                username=newuser.cleaned_data.get('username')
                try:
                    signupdata.objects.get(username=username)
                    print("Username is already exists!")
                    msg="Username is already exists!"
                except signupdata.DoesNotExist:
                    newuser.save()
                    print("Signup Successfully!")
                    msg="Signup Successfully!"
            else:
                print(newuser.errors)
                msg="Error!Something went wrong...."
        elif request.POST.get('login')=='login': #login

            unm=request.POST['username']
            pas=request.POST['password']

            user=signupdata.objects.filter(username=unm,password=pas)
            fnm=signupdata.objects.get(username=unm)
            uid=signupdata.objects.get(username=unm)
            print("Firstname:",fnm.firstname)
            print("Current UID:",uid.id)
            if user:
                print("Login successfully!")
                #request.session['user']=unm
                request.session['user']=fnm.firstname
                request.session['uid']=uid.id
                return redirect('notes')
            else:
                print("Error!Login fail.....Try again")
    return render(request,'index.html',{'user':user,'msg':msg})

def notes(request):
    user=request.session.get('user')
    if request.method=='POST':
        newnote=notesForm(request.POST,request.FILES)
        if newnote.is_valid():
            newnote.save()
            print("Notes submitted")
        else:
            print(newnote.errors)
    return render(request,'notes.html',{'user':user})

@login_required
def profile(request):
    user=request.session.get('user')
    uid=request.session.get('uid')
    cuser=signupdata.objects.get(id=uid)
    if request.method=='POST':
        updateuser=signupform(request.POST,instance=cuser)
        if updateuser.is_valid():
            updateuser.save()
            print("Profile updated!")
            return redirect('notes')
        else:
            print(updateuser.errors)
    return render(request,'profile.html',{'user':user,'cuser':cuser})


def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method=='POST':
        new=feedbackform(request.POST)
        if new.is_valid():
            new.save()
            print("Feedback send successfully!")

            #Email Sending
            otp=random.randint(1111,9999)
            sub="Thank You!"
            msg=f"Dear User!\n\nThanks for your feedback, we will connect shortly!\n\nIf any queries regarding, you can contact us\n\n Your one time password is f{otp}\n\n+91 9724799469 | help@tops-int.com\n\nThanks & Regards!\nTOPS Tech - Rajkot\nwww.tops-int.com"
            from_email=settings.EMAIL_HOST_USER
            #to_email=['kotechamit5@gmail.com','parthhirpara89827@gmail.com','krishnakachhad20@gmail.com','yogitabeladiya2425@gmail.com','rinkalbhad245@gmail.com','janvivora244@gmail.com','vrutikadudhat3@gmail.com','tahjudin597@gmail.com']
            to_email=[request.POST['email']]
            send_mail(subject=sub,message=msg,from_email=from_email,recipient_list=to_email)

            #SMS-OTP Sending
            url = "https://www.fast2sms.com/dev/bulkV2"
            #querystring = {"authorization":"xSJfwu8H9bV6DUX5mdt0GINi3yhoa27kPjn1BTlpOgFQsMcEY4vzPAjNln0oyQOWe6mYbSRCkru4iUqB","variables_values":f"{otp}","route":"otp","numbers":f"{request.POST['phone']}"}
            querystring = {"authorization":"xSJfwu8H9bV6DUX5mdt0GINi3yhoa27kPjn1BTlpOgFQsMcEY4vzPAjNln0oyQOWe6mYbSRCkru4iUqB","message":f"Dear User\nThis msg from TOPS Technologies, Your SS session has been scheduled.Plz visit www.tops-int.com","language":"english","route":"q","numbers":f"{request.POST['phone']}"}
            headers = {
                'cache-control': "no-cache"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)

        else:
            print(new.errors)
    return render(request,'contact.html')

def userlogout(request):
    logout(request)
    return redirect('/')