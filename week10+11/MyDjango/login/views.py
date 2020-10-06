from .form import LoginForm
from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello from MyDjango!")


def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 读取表单的返回值
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                # 登陆用户
                login(request, user)
                return redirect('/')
            else:
                return HttpResponse('登录失败')

    # GET
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, 'form.html', {'form': login_form})
