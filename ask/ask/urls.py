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
from qa import views
from dashing.utils import router
from django.conf.urls import include
#from django.contrib.auth.views import login

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^dashboard/', include(router.urls)),
    url(r'^$', views.main, name='main'),
    url(r'^login/', views.my_login, name='login'),
    url(r'^logout/', views.my_logout, name='logout'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^question/(?P<question_id>[0-9]+)/', views.question, name='question'),
    #url(r'^question/[0-9]+/', test),
    url(r'^ask/', views.ask, name='ask'),
    url(r'^answer/', views.answer, name='answer'),
    url(r'^popular/', views.popular, name='popular'),
    url(r'^new/', views.main, name='main'),
]
