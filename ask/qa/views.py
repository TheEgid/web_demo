from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Answer, Question
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse
from django.urls import reverse
from .forms import AnswerForm, AskForm  #, UserCreateForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect


def test(request, *args, **kwargs):
    return HttpResponse('NU_OK')


def page(request):
    object_list = Question.objects.all().order_by('-pk')
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
    return render(request, 'answers.html',
                  {'page': page,
                   'all_pages': all_pages,
                   'questions': questions,
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
            #user = User.objects.get(username=request.user.username)
            user = User.objects.get(pk=1)
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


def ask(request, *args, **kwargs):
    global user
    if request.method == 'POST':
        # if not request.user.is_authenticated():
        #     return HttpResponseRedirect('/login/')
        form = AskForm(request.POST)
        if form.is_valid():
            #user = User.objects.get(username=request.user.username)
            user = User.objects.get(pk=1)
            question = form.save(user)
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    #user = request.user.username
    author = User.objects.get(pk=1)
    return render(request, 'ask.html',
                  {'form': form, 'author': author})
