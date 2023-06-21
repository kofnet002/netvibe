from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm
from .models import Account
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# from friend.friend_request_status import FriendRequestStatus
from django.conf import settings
from friend.models import FriendList, FriendRequest

# Create your views here.
def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}")
    
    context={}
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            # clean user intput & login user
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, raw_password=raw_password)
            if account:
                login(request, account)
                return redirect('home')

            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect('home')
        else:
            context['registration_form'] = form

    return render(request, 'account/register.html', context)            


def login_view(request, *args, **kwargs):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect('home')
        else:
            context['login_form'] = form     
    return render(request, 'account/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get('next'):
            redirect = str(request.GET.get('next'))
    return redirect


@login_required(login_url='login')
def search_friend(request):
    if request.GET:
        query = request.GET.get('q')
        if len(query) > 0:
            users = Account.objects.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query),
            )

            accounts = []

            for account in users:
                accounts.append((account, False))
         
    context = {
        'users': users,
        'accounts': accounts
    }
    return render(request, "account/search.html", context)


def account_view(request, *args, **kwargs):
    """
        is_self
            is_friend
                -1: NO_REQUEST_SENT
                0: THEM_SENT_TO_YOU
                1: YOU_SENT_TO_THEM
    """

    context = {}

    user_id = kwargs.get('user_id')
    try:
        account = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        return HttpResponse("THat user does not exist")
    
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url

        # Define state templates variables
        is_self = True
        is_friend = False
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False
        
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL

        return render(request, "account/profile.html", context)