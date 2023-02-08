
from django.urls import path
from .views import index, other_page, BBLoginView, ChangeUserInfoView, profile, BBLogoutView
app_name = 'main'
urlpatterns = [
    path('', index, name='index'),
    path('<str:page>/', other_page, name='other'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('account/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/', profile, name='profile'), 
    path('account/logout/', BBLogoutView.as_view(), name='logout'),
    
]

