from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from .forms import UserForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import(
    authenticate,
    login as django_login,
    logout as django_logout,
)


def index(request):
    if not request.user.is_authenticated:
        data = {"username":request.user, "is_authenticated":request.user.is_authenticated}
    else:
        data = {"last_login":request.user.last_login, "username":request.user.username,
        "password":request.user.password,"is_authenticated":request.user.is_authenticated}
    return render(request, "UserService/index.html", context= {"data":data}
    )
@csrf_exempt
def signup(request):
    print("----------singup()--------------")
    if request.method =="POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            django_login(request, new_user)
            return redirect("/")
        else:
            return HttpResponse("UserService/index.html",{"msg":"회원 가입 실패, 다시시도해주세요"})
    else:
        form = UserForm()
        return render(request, "UserService/signup.html",{"form" : form})
    return render(request, "UserService.html")


def login_check(request):
    if request.method =="POST":
        form = LoginForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username = username, password = password)
        if user is not None:
            django_login(request, user)
            return redirect("/")
        else:
            return HttpResponse("UserService/index.html.",{"msg":"로그인 실패, 다시시도해주세요"})
    else:
        form = LoginForm()
        return render(request, "UserService/login.html", {"form":form})

def logout(request):
    django_logout(request)
    return redirect("/")