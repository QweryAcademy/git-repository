"""backend URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    url(r'^$', views.hello, name='home_page'),
    url(r'^add_todo/$', csrf_exempt(views.add_todo), name='add_todo'),
    url(r'^delete_todo/(?P<pk>[0-9]+)/$', csrf_exempt(views.delete_todo), name='delete_todo'),
    url(r'^bulk_update_todos/$', csrf_exempt(views.bulk_update), name='bulk_update'),
    url(r'^update_todo/(?P<pk>[0-9]+)/$', csrf_exempt(views.update_todo), name='update_todo'),
    url(r'^admin/', admin.site.urls),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
