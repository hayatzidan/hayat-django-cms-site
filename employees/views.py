import requests
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from .forms import PhoneLoginForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee, LinkedAccount, ButtonClick
from django.contrib.auth.models import User
# from reversion.models import Version
from decouple import config
from djangocms_versioning.models import Version
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from django.views.decorators.http import require_POST
from urllib.parse import urlencode
# from django.core.exceptions import ValidationError
from django.contrib.auth import logout
from django.conf import settings
from twilio.rest import Client
import random

def delete_employee(request, employee_id): 
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == "POST":
        employee.delete()
        return redirect("employeess")  # Change to the correct URL name of your employee list page



def phone_login_view(request):
    form = PhoneLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(request, phone_number=form.cleaned_data['phone_number'], password=form.cleaned_data['password'])
        if user:
            login(request, user)
            return redirect('employees')
        else:
            form.add_error(None, 'Invalid phone number or password.')
    return render(request, 'employees/login_form.html', {'form': form})



User = get_user_model()

def send_sms(phone, body):
    account_sid = config("TWILIO_ACCOUNT_SID")
    auth_token = config("TWILIO_AUTH_TOKEN")
    twilio_number = config("TWILIO_NUMBER")

    client = Client(account_sid, auth_token)
    message = client.messages.create(  # ✅ we should save it in a ver..
        body=body,
        from_=twilio_number,
        to=str(phone)
    )
    print(f"Twilio message SID: {message.sid}")  

def phone_send_password_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        print(f"Trying to send to: {phone_number}")
        try:
            # to make sure just a temp database
            new_password = str(random.randint(100000, 999999))
            send_sms(phone_number, f"Your login password is: {new_password}")
            request.session['phone_number'] = phone_number
            return redirect('phone_password_login')
        except Exception as e:
            print(f"SMS error: {e}")
            messages.error(request, "Failed to send SMS.")
    return render(request, 'employees/send_password.html')


def phone_password_login_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        phone_number = request.session.get('phone_number')

        user = authenticate(request, phone_number=phone_number, password=password)
        if user:
            login(request, user)
            return redirect('employees')
        else:
            messages.error(request, "Incorrect password.")
    
    return render(request, 'employees/enter_password.html')


def count_visit(request):
    visit = request.session.get('visit',0) + 1
    request.session['visit'] = visit
    return HttpResponse(f"Visit count:{request.session['visit']}")



def show_user_id(request):
    if request.user.is_authenticated:
        return HttpResponse(f"Your user ID is: {request.user.id}")
    else:
        return HttpResponse("You are not logged in.")


@login_required
def social_connections(request):
    accounts = SocialAccount.objects.filter(user=request.user)
    return render(request, 'employees/social_connections.html', {'accounts': accounts})




@require_POST
@login_required
def delete_account(request): 
    user = request.user
    # logout(request)     # log the user out first
    SocialAccount.objects.filter(user=user).delete()

    # delete the userrr
    user.delete()

    # log out after the deletion
    logout(request)
    return redirect('/')







@login_required
def accountt_settings(request):
    accounts = request.user.socialaccount_set.all()
    return render(request, "employees/settings.html", {"accounts": accounts})


@login_required
def unlink_account(request, account_id):
    account = get_object_or_404(SocialAccount, id=account_id, user=request.user)

    # delete the linked social account only
    account.delete()

    # if no more linked accounts remain, deactivate the user and log them out
    if not SocialAccount.objects.filter(user=request.user).exists():
        user = request.user
        
        # 🔥 delete any custom Google/Facebook account models you have linked
        if hasattr(user, "googleaccount"):
            user.googleaccount.delete()
        if hasattr(user, "facebookaccount"):
            user.facebookaccount.delete()

        user.is_active = False
        user.save()
        logout(request)
        return redirect('/')  # ✅ go home

    return redirect('/')



@login_required
def account_settings(request):
    google_account = SocialAccount.objects.filter(
        user=request.user, provider="google"
    ).first()
    facebook_account = SocialAccount.objects.filter(
        user=request.user, provider="facebook"
    ).first()

    return render(request, "employees/settings.html", {
        "google_account": google_account,
        "facebook_account": facebook_account,
    })


@login_required
def accountsettings(request):
    user = request.user  
    # get the linked accounts 
    social_accounts = SocialAccount.objects.filter(user=user)
    
    return render(request, "employees/accountsettings.html", {
        "user": user,
        "social_accounts": social_accounts,
    })


@login_required
def button_view(request):
    user = request.user
    click, created = ButtonClick.objects.get_or_create(user=user)

    if request.method == "POST":
        if not click.clicked:  
            click.clicked = True
            click.save()
        return redirect("button_view")

    total_clicks = ButtonClick.objects.filter(clicked=True).count()
    other_clicks = total_clicks - 1 if click.clicked else total_clicks

    return render(request, "home.html", {
        "clicked": click.clicked,
        "other_clicks": other_clicks
    })


def reels_view(request):
    reels = [
        # TikTok 1
        {
            "type": "tiktok",
            "url": "https://www.tiktok.com/@english.with.me57/video/7514349911165472018",
            "id": "7514349911165472018",
        },
        # Instagram 1
        {
            "type": "instagram",
            "url": "https://www.instagram.com/reel/C1iQp3eMxyz/",
        },
        # Instagram 2 (your new one)
        {
            "type": "instagram",
            "url": "https://www.instagram.com/reel/DO-acfpje2i/",
        },
        # TikTok 2 (your new one)
        {
            "type": "tiktok",
            "url": "https://www.tiktok.com/@english.with.me57/video/7522811276196597010",
            "id": "7522811276196597010",
        },
    ]
    return render(request, "employees/reels.html", {"reels": reels})
