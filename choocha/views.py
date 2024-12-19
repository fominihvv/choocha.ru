from django.http import HttpResponse, HttpResponseNotFound, HttpRequest


# Create your views here.


def index(request) -> HttpResponse:
    return HttpResponse('Типа основной сайт')


def page_not_found(request, exception) -> HttpResponse:
    return HttpResponseNotFound(f'<h1>Страница {request.path} не найдена</h1>')