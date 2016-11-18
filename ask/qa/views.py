from django.shortcuts import render
from django.http import HttpResponse
from models import Question

# Create your views here.

#print(HttpRequest.GET['id'])
def test(request, *args):
    print(type(Question.objects))

    """
    print(request.COOKIES)
    print(request.method)
    print(request.user)
    print(request.META)
    """
    #print(args[0])
    #print(kwargs['pk'])


    return HttpResponse('OK')
