from django.http import HttpResponse, HttpResponseNotFound, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.template import RequestContext


def e_handler404(request, exception):
    print('404')
    print(request)
    return render(request, 'notes/404.html')


def e_handler500(request):
    print('500')
    print(request)
    return render(request, 'notes/500.html')