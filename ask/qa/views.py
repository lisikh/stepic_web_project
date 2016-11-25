from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from models import Question, Answer
from forms import AskForm, AnswerForm, NewUserForm, LoginForm
from models import QuestionManager
#from django.db.models.fields.related import ForeignKey
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse


# Create your views here.

#print(HttpRequest.GET['id'])
def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, limit)
    #paginator.baseurl = 'qa/question/'
    try:
        page = paginator.page(page)

    except Exception:
        page = paginator.page(paginator.num_pages)
    return page, paginator

def test(request, **args):
    """
    print(request.COOKIES)
    print(request.method)
    print(request.user)
    print(request.META)
    """
    #print(args[0])
    #print(kwargs['pk'])
    return HttpResponse('OK')

def main(request):
    print(request.COOKIES)
    page, paginator = paginate(request, Question.objects.new())
    return render(request, 'qa/main.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page
    })

def popular(request):
    page, paginator = paginate(request, Question.objects.popular())
    return render(request, 'qa/main.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page
    })

def question(request, **question):
    id = question['question_id']
    title = get_object_or_404(Question, id=id)
    text = Question.objects.values_list('text', flat=True).get(id=id)
    answers = Answer.objects.filter(question_id=id)
    form = AnswerForm(initial={'question': id})

    return render(request, 'qa/question.html', {
        'title': title,
        'text': text,
        'answers': answers,
        'form': form
    })

@login_required
def ask(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        form._user = request.user
        if form.is_valid():
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'qa/ask_form.html', {
        'form': form
    })

@require_POST
def answer(request):
    form = AnswerForm(request.POST)
    form._user = request.user
    if form.is_valid():
        answer = form.save()
        url = answer.get_url()
        return HttpResponseRedirect(url)

def my_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.cleaned_data['user'])
            return HttpResponseRedirect(reverse('main'))
        else:
            return render(request, 'qa/login.html', {
                'form': form
            })
    else:
        form = LoginForm()
        return render(request, 'qa/login.html', {
            'form': form
        })

def my_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main'))

def signup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        print(dir(form.errors))
        if form.is_valid():
            form.save()
            login(request, form.cleaned_data['user'])
            #password = request.POST['password']
            #user = authenticate(username=user, password=password)
            #print(user, password)
            #if user is not None:
              #  login(request, user)
             #   print('SESSION user is', request.session)
            return HttpResponseRedirect(reverse('main'))
        else:
            return render(request, 'qa/signup.html', {
                'form': form
            })
    else:
        form = NewUserForm()
        return render(request, 'qa/signup.html', {
            'form': form
        })