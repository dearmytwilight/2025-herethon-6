from django.urls import path
from .views.login import login_view
from .views.signup import signup_view
from .views.mypage import mypage_view
from users.views.onboarding import onboarding_view, onboarding_view2, onboarding_view3, finish_onboarding

app_name = "users"

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('mypage/', mypage_view, name='mypage'),
    path('onboarding/1/', onboarding_view, name='onboarding1'),
    path('onboarding/2/', onboarding_view2, name='onboarding2'),
    path('onboarding/3/', onboarding_view3, name='onboarding3'),
    path('onboarding/finish/', finish_onboarding, name='finish_onboarding')
]