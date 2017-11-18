"""backsplice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin, auth
from website import views

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$',  views.home, name='home'),
    url(r'^scouts/$', views.scouts, name='scouts'),
    url(r'^instructors/$', views.instructors, name='instructors'),
    url(r'^pending_requests/$', views.pending_requests, 
        name='pending_requests'),
    url(r'^create_paperwork/$', views.create_paperwork,
        name='create_paperwork'),
    url(r'^course_catalog/$', views.course_catalog, 
        name='course_catalog'),
    url(r'^course_catalog/edit/$', views.edit_course_catalog, 
        name='edit_course_catalog'),
    url(r'^course_catalog/import/$', views.import_course_catalog, 
        name='import_course_catalog'),
    url(r'^course_catalog/import/review/$', views.review_course_catalog, 
        name='review_course_catalog'),
]
