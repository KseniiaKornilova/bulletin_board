from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView

# Create your views here.
# Вывод главной страницы
def index(request):
    return render(request, 'main/index.html')

# Вывод страницы "о сайте"
def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

# Реализация входа на сайт
class BBLoginView(LoginView):
    template_name = 'main/login.html'
