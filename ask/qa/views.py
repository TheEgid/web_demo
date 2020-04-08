from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Answer, Question
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.contrib import auth
from django.contrib import messages

from .forms import AnswerForm, AskForm, LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Answer

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login


def test(request, *args, **kwargs):
    return HttpResponse('NU_OK')


def page(request):
    object_list = Question.objects.all().order_by('-pk')
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        user_id = request.session['_auth_user_id']
        user = User.objects.get(pk=user_id) or "Not authorized"
    except KeyError:
        user = "Not authorized"
    #breakpoint()
    if not page:
        page = 1
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    all_pages = int(paginator.num_pages)
    return render(request, 'answers.html',
                  {'page': page,
                   'all_pages': all_pages,
                   'questions': questions,
                   'user': user,
                   })


def popular_page(request):
    object_list = Question.objects.popular()
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    if not page:
        page = 1
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    all_pages = int(paginator.num_pages)
    return render(request, 'answers_populars.html',
                  {'page': page,
                   'all_pages': all_pages,
                   'questions': questions,
                   })


def question(request, slug):
    global question
    global answers
    form = AnswerForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            if not request.user.is_authenticated:
                return HttpResponseRedirect('/login/')
            user_id = request.session['_auth_user_id']
            user = User.objects.get(pk=user_id) or "Not authorized"
            form.save(user)
            url = reverse('question',
                          args=(form.cleaned_data['question_id'],))
            return HttpResponseRedirect(url)

    question = get_object_or_404(Question, id=slug)
    answers = Answer.objects.filter(question_id=question.id)
    author = User.objects.get(pk=1)
    return render(request, 'question.html',
                  {'form': form,
                   'author': author,
                   'question': question,
                   'answers': answers})


# @login_required
def ask(request, *args, **kwargs):
    global user
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/')
        form = AskForm(request.POST)
        if form.is_valid():
            user_id = request.session['_auth_user_id']
            user = User.objects.get(pk=user_id) or "Not authorized"
            question = form.save(user)
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
        user = request.user.username
    return render(request, 'ask.html',
                  {'form': form, 'user': user})


def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(
                username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Disabled account')
    else:
        login_form = LoginForm()
    return render(request, 'login.html', {'form': login_form})


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        username = form.cleaned_data.get('username')
        my_password = form.cleaned_data.get('password1')
        this_user = authenticate(username=username, password=my_password)
        login(request, this_user)
        return redirect('/ask')
    else:
        form = RegisterForm()
        return render(request, 'signup.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect('/page')


# def user_login(request):
#     global user
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'],
#                                 password=cd['password'])
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponse('Authenticated successfully')
#             else:
#                 return HttpResponse('Disabled account')
#         else:
#             return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})


#
#
# def user_login(request):
#     registForm = RegistForm()
#     if request.method == 'GET':
#         loginForm = LoginForm()
#         return render(request, 'account.html', {'loginForm': loginForm, 'registForm': registForm})
#     else:
#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
#         loginForm = LoginForm(
#             {'username': username,
#              'password': password,})
#         if not loginForm.is_valid():
#             return render(request, 'index.html', {'registForm': registForm, 'loginForm': loginForm})
#         else:
#             user = auth.authenticate(request, username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return render(request, 'index.html', {'username': user.username})
#             else:
#                 print(user)
#                 return render(request, 'account.html',
#                                 {'loginForm': loginForm, 'password_is_wrong': True, 'registForm': registForm})
#
#

#
#
# def account(request):
#     registerForm = RegistForm()
#     loginForm = LoginForm()
#     return render(request, 'account.html', {'registForm': registerForm, 'loginForm': loginForm})


# def register(request):
#     loginForm = LoginForm()
#     if request.method == "POST":
#
#         username = request.POST.get('username', None)
#         email = request.POST.get('email', None)
#         password = request.POST.get('password', None)
#         re_password = request.POST.get('re_password', None)
#         errors = []
#
#         registerForm = RegisterForm(
#             {'username': username, 'password': password, 're_password': re_password, 'email': email})
#         if not registerForm.is_valid():
#             return render(request, 'signup.html', {'registForm': registerForm, 'loginForm': loginForm})
#         if password != re_password:
#             errors.append('Two different passwords')
#             return render(request, 'signup.html',
#                           {'form': registerForm, 'errors': errors, 'loginForm': loginForm})
#
#         filterResult = User.objects.filter(username=username)
#         if len(filterResult) > 0:
#             errors.append('User name already exists')
#             return render(request, 'signup.html',
#                           {'form': registerForm, 'errors': errors, 'loginForm': loginForm})
#
#         emailfilter = User.objects.filter(email=email)
#         if len(emailfilter) > 0:
#             errors.append('The mailbox is already in use')
#             return render(request, 'signup.html',
#                           {'form': registerForm, 'errors': errors, 'loginForm': loginForm})
#
#         #user = User.objects.create_user(username=username, password=password, email=email)
#         breakpoint()
#
#         user.save()
#
#         newUser = auth.authenticate(request, username=username, password=password)
#         if newUser is not None:
#             auth.login(request, newUser)
#             return render(request, 'ask.html', {'username':username})
#         else:
#             return render(request, 'signup.html',
#                           {'form': registerForm, 'errors': errors, 'loginForm': loginForm})
#     else:
#         # loginForm = LoginForm()
#         registerForm = RegisterForm()
#         #breakpoint()
#         return render(request, 'signup.html', {'form': registerForm, 'loginForm': loginForm})
