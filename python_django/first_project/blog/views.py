from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)


# Create your views here.


def index(request: HttpRequest):
    header = "Данные пользователя"
    user = {"name": "Ильфатей", "age": 39}
    lang = ["javaScript", "python"]
    address = ("Кул Гали", 36, 36)
    typed_lang = ("typeScript", "GO", "C#")

    data = {
        "header": header,
        "user": user,
        "lang": lang,
        "address": address,
        "typed_lang": typed_lang,
        "text": "<h3>Экранирование</h3>",
        "site": "Stepik.org",
    }

    return TemplateResponse(request, "blog/index.html", context=data)


def acceess(request: HttpRequest, age: int = None):
    if age not in range(1, 111) or age == None:
        return HttpResponseBadRequest("Некорректные данные!")
    if age > 17:
        return HttpResponse("Доступ разрешен")
    else:
        return HttpResponseForbidden("Доступ запрещен: вы еще сосунок!")


def about(request: HttpRequest):
    return render(request, "blog/about.html", context={"site": "Stepik"})


def contact(request: HttpRequest):
    return HttpResponseRedirect("/about/")


def details(request: HttpRequest):
    return HttpResponsePermanentRedirect("/")


def products(request: HttpRequest, id: int = 0):
    return HttpResponse(f"<h2>Список товаров {id}</h2>")


def new(request: HttpRequest, id: int):
    return HttpResponse("<h2>Новые товары</h2>")


def top(request: HttpRequest, id: int):
    return HttpResponse("<h2>Новые популярные товары</h2>")


def user(request: HttpRequest):
    age = request.GET.get("age", 0)
    name = request.GET.get("name", "undefined")
    return HttpResponse(f"<h2>Имя: {name}, Вовзраст: {age}</h2>")
