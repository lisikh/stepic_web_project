"""ask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import logout, login
from qa import views
from django.views.generic import TemplateView
# from dashing.utils import router
from django.conf.urls import include
#from django.contrib.auth.views import login

urlpatterns = [
    # Show just some template without creating your own view for it!
    url(r'^about/', TemplateView.as_view(template_name='qa/base.html')),

    url(r'^admin/', admin.site.urls),
    # url(r'^dashboard/', include(router.urls)),
    url(r'^$', views.main, name='main'),
    url(r'^login/', login, {'template_name': 'qa/login.html'}, name='login'),
    # url(r'^login/', views.MyLogin.as_view(), name='login'),
    # url(r'^logout/', views.my_logout, name='logout'),
    url(r'^logout/', logout, name='logout'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^question/(?P<question_id>[0-9]+)/', views.question, name='question'),
    #url(r'^question/[0-9]+/', test),
    url(r'^ask/', views.ask, name='ask'),
    url(r'^answer/', views.answer, name='answer'),
    url(r'^popular/', views.popular, name='popular'),
    url(r'^new/', views.main, name='main'),
]
