from django.shortcuts import render
from django.http import HttpResponse
from models import Question, Answer
from models import QuestionManager
from django.db.models.fields.related import ForeignKey
# Create your views here.

#print(HttpRequest.GET['id'])
def test(request, *args):
    author = Answer._meta.get_field('author')
    print(type(author))
    print (isinstance(author, ForeignKey))

    """
    print(request.COOKIES)
    print(request.method)
    print(request.user)
    print(request.META)
    """
    #print(args[0])
    #print(kwargs['pk'])


    return HttpResponse('OK')
