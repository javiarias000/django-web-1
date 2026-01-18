from django.urls import path
from portafolio import views
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

urlpatterns = [
    path('set-language/', set_language, name='set_language'),
]

urlpatterns += i18n_patterns(
    path('', views.home, name='home'),
    path('education/', views.education, name='education'),
)