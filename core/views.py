from django.shortcuts import render, redirect
from django.http import HttpResponse
from core.models import KYC, Account
from core.forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CreditCardForm
from core.models import CreditCard, Notification, Transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from guest_user.decorators import allow_guest_user
from core.models import User
from core.forms import UserRegisterForm


def index(request):
    if request.user.is_authenticated:
        return redirect("core:account")
    return render(request, "core/index.html")

def contact(request):
    return render(request, "core/contact.html")

def about(request):
    return render(request, "core/about.html")
    
# @login_required
def account(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("core:kyc-reg")
        
        account = Account.objects.get(user=request.user)
    else:
        messages.warning(request, "You need to login to access the dashboard")
        return redirect("core:sign-in")

    context = {
        "kyc":kyc,
        "account":account,
    }
    return render(request, "account/account.html", context)

@login_required
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=user)

    try:
        kyc = KYC.objects.get(user=user)
    except:
        kyc = None
    
    if request.method == "POST":
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(request, "KYC Form submitted successfully, In review now.")
            return redirect("core:account")
    else:
        form = KYCForm(instance=kyc)
    context = {
        "account": account,
        "form": form,
        "kyc": kyc,
    }
    return render(request, "account/kyc-form.html", context)


def dashboard(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("core:kyc-reg")
        
        recent_transfer = Transaction.objects.filter(sender=request.user, transaction_type="transfer", status="completed").order_by("-id")[:1]
        recent_recieved_transfer = Transaction.objects.filter(reciever=request.user, transaction_type="transfer").order_by("-id")[:1]


        sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="transfer").order_by("-id")
        reciever_transaction = Transaction.objects.filter(reciever=request.user, transaction_type="transfer").order_by("-id")

        request_sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="request")
        request_reciever_transaction = Transaction.objects.filter(reciever=request.user, transaction_type="request")
        
        
        account = Account.objects.get(user=request.user)
        credit_card = CreditCard.objects.filter(user=request.user).order_by("-id")

        if request.method == "POST":
            form = CreditCardForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user 
                new_form.save()
                
                Notification.objects.create(
                    user=request.user,
                    notification_type="Added Credit Card"
                )
                
                card_id = new_form.card_id
                messages.success(request, "Card Added Successfully.")
                return redirect("core:dashboard")
        else:
            form = CreditCardForm()

    else:
        messages.warning(request, "You need to login to access the dashboard")
        return redirect("core:sign-in")

    context = {
        "kyc":kyc,
        "account":account,
        "form":form,
        "credit_card":credit_card,
        "sender_transaction":sender_transaction,
        "reciever_transaction":reciever_transaction,

        'request_sender_transaction':request_sender_transaction,
        'request_reciever_transaction':request_reciever_transaction,
        'recent_transfer':recent_transfer,
        'recent_recieved_transfer':recent_recieved_transfer,
    }
    return render(request, "account/dashboard.html", context)
    
def RegisterView(request):
    if request.user.is_authenticated:
        messages.warning(request, f"You are already logged in.")
        return redirect("core:account")
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # form.save()
            new_user = form.save() # new_user.email
            username = form.cleaned_data.get("username")
            # username = request.POST.get("username")
            messages.success(request, f"Hey {username}, your account was created successfully.")
            # new_user = authenticate(username=form.cleaned_data.get('email'))
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("core:account")

    else:
        form = UserRegisterForm()
    context = {
        "form": form
    }
    return render(request, "userauths/sign-up.html", context)

def LoginView(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None: # if there is a user
                login(request, user)
                messages.success(request, "You are logged.")
                return redirect("core:account")
            else:
                messages.warning(request, "Username or password does not exist")
                return redirect("core:sign-in")
        except:
            messages.warning(request, "User does not exist")

    if request.user.is_authenticated:
        messages.warning(request, "You are already logged In")
        return redirect("core:account")
        
    return render(request, "userauths/sign-in.html")

@allow_guest_user
def GuestLoginView(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None: # if there is a user
                login(request, user)
                messages.success(request, "You are logged.")
                return redirect("core:account")
            else:
                messages.warning(request, "Username or password does not exist")
                return redirect("core:sign-in")
        except:
            messages.warning(request, "User does not exist")

    if request.user.is_authenticated:
        messages.warning(request, "You are already logged In")
        return redirect("core:account")
        
    return render(request, "userauths/sign-in.html")

def logoutView(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("core:sign-in")
