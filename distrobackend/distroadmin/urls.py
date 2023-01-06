from django.urls import path
from distroadmin.views import RegisterDistroAdminView
urlpatterns = [
    path('register-admin/', RegisterDistroAdminView.as_view(), name='register-admin'),

]