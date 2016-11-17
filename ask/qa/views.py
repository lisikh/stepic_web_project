from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

#print(HttpRequest.GET['id'])
def test(request, *args):
    """
    print(request.COOKIES)
    print(request.method)
    print(request.user)
    print(request.META)
    """
    #print(args[0])
    #print(kwargs['pk'])


    return HttpResponse('OK')
