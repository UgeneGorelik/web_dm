from django.db import models
from django.db.models import Max,Min
from django.contrib.postgres.indexes import HashIndex
from django.contrib.auth.models import AbstractUser, BaseUserManager
from copy import deepcopy


import json
from ds_management.string_constraints.string_constraints import *


class ItemCategory(models.Model):
    category_name = models.CharField(max_length=250, unique=True, choices=STRUCTURE_CHOICES)

    def __str__(self):
        return self.category_name

    def __unicode__(self):
        return self.category_name


class Item(models.Model):
    item_name = models.CharField(max_length=250, unique=True)
    category_name = models.ForeignKey(ItemCategory,
                                        choices=STRUCTURE_CHOICES,
                                         on_delete=models.CASCADE,
                                         default=1
                                        )

    def __str__(self):
        return self.item_name


class ItemElementManager(BaseUserManager):

    def pop(self,item_id):
        structure_type = Item.objects.get(pk=item_id).category_name.category_name
        if structure_type and structure_type is DataStructures.queue or DataStructures.stack:
           response_result = StackQueue.objects.pop(item_id)
        return response_result

    def add_new_element(self,item_id, element_data):
        structure_type = Item.objects.get(pk=item_id).category_name.category_name
        element = ItemElement.objects.create(item_id=item_id,
                                             element_data=element_data,
                                             )

        if structure_type and structure_type is \
                DataStructures.queue or DataStructures.stack or DataStructures.list:
            new_element = StackQueue.objects.push(item_id=item_id,
                                                  element_id=element.id,
                                                  structure_type=structure_type

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


class StackQueueManager(models.Manager):
    def push(self, item_id, element_id,structure_type):
        if self.is_empty(item_id):
            new_element = self.create(item_id=item_id,
                                                    element_id=element_id,
                                                    position=0
                                                    )

        else:
            element_to_push_index = self.filter(item_id=item_id).aggregate(Max(position_str))['position__max']
            new_index = element_to_push_index +1
            new_element = self.create(item_id=item_id,
                                       element_id=element_id,
                                        position=new_index
                                                        )

        return new_element

    def pop(self,item_id):
        item = Item.objects.get(pk=item_id)
        structure_type = item.category_name.category_name
        element_to_pop = None
        element_to_pop_index = None

        if not self.is_empty(item_id):
            if structure_type == DataStructures.stack:
                element_to_pop_index = self.filter(item_id=item_id).aggregate(Max(position_str))['position__max']
            elif structure_type in [DataStructures.queue,DataStructures.list]:
                element_to_pop_index = self.filter(item_id=item_id).aggregate(Min(position_str))['position__min']

            new_instance = self.clone_and_delete_element(element_to_pop_index,item_id)

            return new_instance

    def clone_and_delete_element(self,position,item_id):
        element_to_pop = self.get(position=position, item_id=item_id)
        item_element_to_delete = ItemElement.objects.get(id=element_to_pop.element_id)
        new_instance = deepcopy(item_element_to_delete)
        element_to_pop.delete()
        item_element_to_delete.delete()
        return new_instance


    def is_empty(self,item_id):
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




