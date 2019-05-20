from django.urls import path, include
from . import views

urlpatterns =[
    path('', views.index),
    path('register',views.register),
    path('join',views.join),
    path('login',views.verify),
    path('users/<num>',views.user),
    path('users/<num>/post',views.post),
    path('users/<num>/comment',views.comment),
    path('users/<num>/follow',views.follow),
    path('users/<num>/update',views.update),
    path('splash',views.home),
    path('logout',views.reset),
    path('post',views.local_post),
    path('comment',views.local_comment),
    path('<cat>/results/<tag>',views.tag_sort),
    path('<cat>/results',views.cat_sort),
    path('search',views.search),
    path('delete',views.destroy),
    path('users/<num>/unfollow', views.unfollow),

]