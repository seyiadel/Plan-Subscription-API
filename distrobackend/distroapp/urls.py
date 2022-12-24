from django.urls import path
from distroapp.views import PlanView

urlpatterns = [
    path('plan/', PlanView.as_view(), name="plan"),
]