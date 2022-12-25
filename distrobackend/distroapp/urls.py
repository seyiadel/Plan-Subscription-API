from django.urls import path
from distroapp.views import PlanView, PlanDetailView, RegisterDistroUserView

urlpatterns = [
    path('plan/', PlanView.as_view(), name="plan"),
    path('plan-detail/<int:id>/', PlanDetailView.as_view(), name="plan-detail"),
    path('register/', RegisterDistroUserView.as_view(), name="register")
    
]