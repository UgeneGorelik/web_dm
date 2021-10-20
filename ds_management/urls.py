"""
Book: Django RESTful Web Services
Author: Gaston C. Hillar - Twitter.com/gastonhillar
Publisher: Packt Publishing Ltd. - http://www.packtpub.com
"""

from django.urls import path,re_path
from ds_management.views import item_view,item_element_view
from ds_management.views import ItemViewSet
from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from django.contrib import admin


router = DefaultRouter()
router.register(r'api/list_items', ItemViewSet)


urlpatterns = [
    path('items', item_view),
    re_path(r'^items/(?P<pk>[0-9]+)$', item_element_view),
    url(r'', include(router.urls)),
    path('admin/', admin.site.urls)
]