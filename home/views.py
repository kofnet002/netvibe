from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.models import Account


# Create your views here.
@login_required(login_url='/login')
def index(request):
    user = request.user.username
    all_users = Account.objects.exclude(username=user)

    context = {
        'all_users': all_users,
    }

    return render(request, 'home/home.html', context)


def save_post(request):
    if request.method == 'POST':
        user = request.user.username
        caption = request.POST.get('caption')
        _file = request.FILES.get('test')
        print(user, caption, _file)
    return render(request, 'home/home.html')
