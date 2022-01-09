from django.urls import path
from .views import RegistroView, PerfilView, CambioPasswordView
# from django.contrib.auth import views as auth_views
from .views import PerfilUpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

registration_patterns = ([
    path('registro/', RegistroView,name='registro'),
    path('perfil/', login_required(PerfilView),name='perfil'),
    path('update_perfil/', login_required(PerfilUpdateView),name='update_perfil'),
    # path('password_change/',auth_views.PasswordChangeView.as_view(
    # 	template_name = 'registration/cambio_password.html',
    # 	success_url = '/accounts/login/')
    # 	,name='cambio_password')
    path('password_change/',login_required(CambioPasswordView),name='cambio_password')
],'registration')