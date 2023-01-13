from django.urls import path
from distroapp.views import IntroductionView, PlanView, PlanDetailView, RegisterDistroUserView, LoginDistroUserView, DistroUserView, ProcessDistroPlan,VerifyDistroPayment
from knox.views import LogoutView, LogoutAllView

urlpatterns = [
    path('',IntroductionView.as_view(), name="main"),
    path('plan/', PlanView.as_view(), name="plan"),
    path('plan-detail/<int:id>/', PlanDetailView.as_view(), name="plan-detail"),
    path('register/', RegisterDistroUserView.as_view(), name="register"),
    path('login/',LoginDistroUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-all/',LogoutAllView.as_view(), name='logout_all'),
    path('user/', DistroUserView.as_view(), name='user'),
    path('pay-now/<int:plan_id>/', ProcessDistroPlan.as_view(), name='pay-now' ),
    path('verify-payment/<str:reference>/', VerifyDistroPayment.as_view(), name='verify_payment'),
]