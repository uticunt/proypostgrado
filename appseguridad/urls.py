'''from rest_framework import routers
from appseguridad.api import UserViewSet
from django.urls import path,include



router_user = routers.DefaultRouter()
router_user.register(r'api/user', UserViewSet,'usuarios')'''


'''urlpatterns =[
    path('',include( router_user.urls)),
]
'''
'''
from django.urls import path,include,re_path
from appseguridad import api

urlpatterns =[
    path('login/',include(api.login)),
]'''