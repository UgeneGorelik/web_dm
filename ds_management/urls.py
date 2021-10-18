"""
Book: Django RESTful Web Services
Author: Gaston C. Hillar - Twitter.com/gastonhillar
Publisher: Packt Publishing Ltd. - http://www.packtpub.com
"""

from django.urls import path,re_path
from ds_management.views import add_item,add_item_element
from ds_management.views import ItemCategoryViewSet,StackQueueViewSet
from ds_management.views import ItemViewSet
from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include


router = DefaultRouter()
router.register(r'api/list_items', ItemViewSet)
router.register(r'api/list_categories', ItemCategoryViewSet)
router.register(r'api/list_stack_queue', StackQueueViewSet)


urlpatterns = [
    path('items', add_item),
    re_path(r'^items/(?P<pk>[0-9]+)$', add_item_element),
    url(r'', include(router.urls)),
]