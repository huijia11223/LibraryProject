from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^login/$',views.login),
    url(r'^queryBook/$', views.queryBook),
    url(r'^borrowBook/$', views.borrowBook),
    url(r'^returnBook/$', views.returnBook),
    url(r'^addBook/$', views.addBook),
    url(r'^editReader/(\d+)/$', views.editReader),
    url(r'^readerlist/$',views.readerlist),
    url(r'^index/$',views.index),
   url(r'^returnbook/$',views.returnBook)

]
