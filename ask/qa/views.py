from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from models import Question, Answer
from models import QuestionManager
#from django.db.models.fields.related import ForeignKey
from django.core.paginator import Paginator

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
    return render(request, 'qa/question.html', {
        'title': title,
        'text': text,
        'answers': answers
    })
