
from django.urls import path
from .views import index, other_page, BBLoginView

app_name = 'main'
urlpatterns = [
    path('', index, name='index'),
    path('<str:page>/', other_page, name='other'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
]

