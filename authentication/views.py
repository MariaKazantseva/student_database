from django.shortcuts import redirect
from django.template.response import TemplateResponse
from authentication.forms import LoginForm
from django.contrib.auth import authenticate, login


def login_view(request):
    form = LoginForm(request.POST or None)
    params = {
        'form': None,
        'message': None
    }
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                params['message'] = 'Неверно введенные данные'
        else:
            params['message'] = 'Заполните все поля'
    params['form'] = form
    return TemplateResponse(request, "registration/login.html", params)