from django.urls import path
from distroadmin.views import RegisterDistroAdminView, LoginAdminView, PlanAdminView, PlanDetailAdminView
urlpatterns = [
    path('register-staff/', RegisterDistroAdminView.as_view(), name='register-admin'),
    path('login-staff/',LoginAdminView.as_view(), name='staff-login'),
    path('plan-staff/', PlanAdminView.as_view(), name='plan-staff'),
    path('plan-detail-staff/<int:id>', PlanDetailAdminView.as_view(), name='plan-detail-staff')
]