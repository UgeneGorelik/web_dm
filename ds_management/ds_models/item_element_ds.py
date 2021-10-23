from ds_management.models import ItemElement,Item,StackQueue

from django.db import models

from ds_management.string_constraints.string_constraints import *

#
# class ItemElemenManager(models.Manager):
#     @staticmethod
#     def pop(item_id) -> Dict:
#         """
#         remove last element from DS
#
#         :param item_id:
#         :return:
#         """
#
#         response_ result: Dict = StackQueueDs.pop(item_id)
#         return response_result
#
#     @staticmethod
#     def peek(item_id) -> Dict:
#         """
#        see last item in DS
#
#         :param item_id:
#         :return:
#         """
#
#         response_result: Dict = StackQueueDs.pop(item_id, remove_item=False)
#         return response_result
#
#     @staticmethod
#     def push(item_id, element_data)->Dict:
#         element: ItemElement = ItemElement.objects.create(item_id=item_id,
#                                              element_data=element_data,
#                                              )
#         new_element: Dict = StackQueueDs.push(item_id=item_id,
#                                               element_id=element.id,
#                                               )
#
#         return new_element
