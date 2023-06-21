# from django.shortcuts import render
# from account.models import Account
# from django.db.models import Q
# from django.contrib.auth.decorators import login_required


# # Create your views here.
# @login_required(login_url='login')
# def search_friend(request):
#     if request.GET:
#         query = request.GET.get('q')

#         users = Account.objects.filter(
#             Q(username__icontains=query) |
#             Q(email__icontains=query),
#         )
     
#         print(users)
    
#     context = {
#         'users': users,
#     }
#     return render(request, "friend/search.html", context)