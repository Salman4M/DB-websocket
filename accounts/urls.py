from django.urls import path
from accounts import views


app_name='accounts'

urlpatterns = [
    path('home/',views.home_view,name='home'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('create/',views.account_create_view,name='acc_create'),
    path('profile/',views.profile_view,name='profile'),
    path('profile/update/',views.profile_update_view,name='profile_update'),
    path('profile/onboarding/',views.profile_update_view,name='profile_onboarding'),

]
