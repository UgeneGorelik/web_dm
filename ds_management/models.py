from django.db import models
from django.db.models import Max, Min
from django.contrib.postgres.indexes import HashIndex
from django.contrib.auth.models import  BaseUserManager
from copy import deepcopy
from typing import Dict

import json
from ds_management.string_constraints.string_constraints import *


class ItemCategory(models.Model):
    category_name: models.CharField = models.CharField(max_length=250, unique=True, choices=STRUCTURE_CHOICES)

    def __str__(self) -> models.CharField:
        return self.category_name

    def __unicode__(self)-> models.CharField:
        return self.category_name


class Item(models.Model):
    item_name: models.CharField = models.CharField(max_length=250, unique=True)
    category_name: models.ForeignKey = models.ForeignKey(ItemCategory,
                                                         choices=STRUCTURE_CHOICES,
                                                         on_delete=models.CASCADE,
                                                         default=1
                                                         )
    owner: models.ForeignKey = models.ForeignKey(
                                                'auth.User',
                                                related_name='items',
                                                on_delete=models.CASCADE,
                                                default=0
                                                )

    class Meta:
        unique_together = ('owner', 'item_name')

    def __str__(self)->models.CharField:
        return self.item_name


class ItemElementManager(BaseUserManager):
    @staticmethod
    def pop(item_id) -> Dict:
        """
        remove last element from DS

        :param item_id:
        :return:
        """

        response_result: Dict = None
        structure_type: str = Item.objects.get(pk=item_id).category_name.category_name
        if structure_type and structure_type is DataStructures.queue or DataStructures.stack:
            response_result: Dict = StackQueue.objects.pop(item_id)
        return response_result
    @staticmethod
    def peek(item_id) -> Dict:
        """
       see last item in DS

        :param item_id:
        :return:
        """

        response_result: Dict = None
        structure_type: str = Item.objects.get(pk=item_id).category_name.category_name
        if structure_type and structure_type is DataStructures.queue or DataStructures.stack:
            response_result: Dict = StackQueue.objects.pop(item_id,remove_item=False)
        return response_result

    def clone_element(self, element_id):
        item_element_to_delete: ItemElement = ItemElement.objects.get(id=element_id)
        new_instance: ItemElement = deepcopy(item_element_to_delete)
        return new_instance
    @staticmethod
    def add_new_element(item_id, element_data)->Dict:
        structure_type: str = Item.objects.get(pk=item_id).category_name.category_name
        element: ItemElement = ItemElement.objects.create(item_id=item_id,
                                                          element_data=element_data,
                                                          )

        if structure_type and structure_type is \
                DataStructures.queue or DataStructures.stack or DataStructures.list:
            new_element: Dict = StackQueue.objects.push(item_id=item_id,
                                                        element_id=element.id,
                                                        )

            return new_element


class ItemElement(models.Model):
    objects = ItemElementManager()
    item = models.ForeignKey(
        Item,
        related_name='item_elements',
        on_delete=models.CASCADE,
        default=''
    )
    element_data = models.JSONField(default=dict)
    element_value = models.IntegerField(default=0)

    def __str__(self):
        return json.dumps(self.element_data)


# todo to implement as linked list:https://isaaccomputerscience.org/concepts/dsa_datastruct_stack?examBoard=all&stage=all
class StackQueueManager(models.Manager):

    def push(self, item_id, element_id):
        """
        push new element for item:
        create new one
        :param item_id:
        :param element_id:
        :return:
        """
        if self.is_empty(item_id):
            new_element: ItemElement = self.create(item_id=item_id,
                                                   element_id=element_id,
                                                   position=0
                                                   )

        else:
            element_to_push_index: int = self.filter(item_id=item_id).aggregate(Max(position_str))['position__max']
            new_index: int = element_to_push_index + 1
            new_element: ItemElement = self.create(item_id=item_id,
                                                   element_id=element_id,
                                                   position=new_index
                                                   )

        return new_element

    # todo to implement as linked list:https://isaaccomputerscience.org/concepts/dsa_datastruct_stack?examBoard=all&stage=all
    def pop(self, item_id, remove_item = True) -> ItemElement:
        item: Item = Item.objects.get(pk=item_id)
        structure_type: str = item.category_name.category_name
        element_to_pop_index = None

        if not self.is_empty(item_id):
            if structure_type == DataStructures.stack:
                element_to_pop_index: int = self.filter(item_id=item_id).aggregate(Max(position_str))[position__max_str]
            elif structure_type in [DataStructures.queue, DataStructures.list]:
                element_to_pop_index: int = self.filter(item_id=item_id).aggregate(Min(position_str))[position__min_str]
            element_to_pop: ItemElement = self.get(position=element_to_pop_index, item_id=item_id)
            element_to_pop_element_id: int = element_to_pop.element_id
            new_instance = ItemElement.objects.clone_element(element_to_pop_element_id)
            if remove_item:
                element_to_pop.delete()
                item_element_to_delete: ItemElement = ItemElement.objects.get(id=element_to_pop_element_id)
                item_element_to_delete.delete()

            return new_instance



    # todo to implement as linked list:https://isaaccomputerscience.org/concepts/dsa_datastruct_stack?examBoard=all&stage=all
    def is_empty(self, item_id) ->bool:
        """
        check if data structure have any element left
        :param item_id:
        :return: item element
        """
        have_items = self.filter(item_id=item_id).exists()
        return not have_items


class StackQueue(models.Model):
    position = models.IntegerField()
    item = models.ForeignKey(
        Item,
        related_name='+',
        on_delete=models.CASCADE)
    element = models.ForeignKey(
        ItemElement,
        related_name='+',
        on_delete=models.CASCADE)
    objects = StackQueueManager()

    class Meta:
        unique_together = ('item_id', 'position',)

        indexes = [HashIndex(fields=['item']),
                   models.Index(fields=['element'])
                   ]
