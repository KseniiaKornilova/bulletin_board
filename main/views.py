from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy

from .models import AdvUser
from .forms import ChangeUserInfoForm, RegisterUserForm
from .utilities import signer


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

# Реализация изменения данных пользователя
class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


# Реализация изменения пароля 
class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'

# Реализация регистрации пользователя
class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')

# Реализация вывода страницы с сообщением об успешноц регистрации 
class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'

# Реализация активациюю пользователя
def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


# Реализация удаления пользователя
class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


# Реализация запроса письма для сброса пароля 
class PasswordResetUserView(PasswordResetView):
    template_name = 'main/password_reset.html'
    subject_template_name = 'email/password_reset_subject.txt'
    email_template_name = 'email/password_reset_body.txt'
    success_url = reverse_lazy('main:password_reset_done')


# Вывод страницы с сообщением об успешной отправке письма для сброса пароля
class PasswordResetUserDoneView(PasswordResetDoneView):
    template_name = 'main/password_reset_done.html'


# Реализация сброса пароля
class PasswordResetConfirmUserView(PasswordResetConfirmView):
    template_name = 'main/password_reset_confirm.html'
    success_url = reverse_lazy('main:password_reset_complete')


# Вывод страницы с сообщением об успешном сбросе пароля
class PasswordResetCompleteUserView(PasswordResetCompleteView):
    template_name = 'main/password_reset_complete.html'

        

