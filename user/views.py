from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import LoginForm, RegisterForm

User = get_user_model()


def index(request):
    return render(request, "index.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")

            user = authenticate(username = username, password = raw_password)
            if user is not None:
                msg = "로그인 성공"
                login(request, user)
            return redirect('/')
        # TODO: 1. /login로 접근하면 로그인 페이지를 통해 로그인이 되게 해주세요
        # TODO: 2. login 할 때 form을 활용해주세요						
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    # TODO: 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요						
    return HttpResponseRedirect("/")


# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
@login_required
def user_list_view(request):
    users = User.objects.order_by("-register_date").all()
    # TODO: 7. /users 에 user 목록을 출력해주세요

    paginator = Paginator(users, 3)
    page = request.GET.get('page')
    user = paginator.get_page(page)
    # TODO: 9. user 목록은 pagination이 되게 해주세요
    return render(request, "users.html", {"users": user})
