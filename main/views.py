from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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

# Вывод страницы профиля пользователя
@login_required
def profile(request):
    return render(request, 'main/profile.html')

# Реализация выхода с сайта
class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'

