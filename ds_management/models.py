from django.db import models
from django.contrib.postgres.indexes import HashIndex
from django.contrib.auth.models import BaseUserManager
from ds_management.string_constraints.string_constraints import *
from typing import Dict

import json


class ItemCategory(models.Model):
    category_name: models.CharField = models.CharField(max_length=250, unique=True, choices=STRUCTURE_CHOICES)

    def __str__(self) -> models.CharField:
        return self.category_name

    def __unicode__(self) -> models.CharField:
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

    def __str__(self) -> models.CharField:
        return self.item_name


class ItemElement(models.Model):
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

    class Meta:
        unique_together = ('item_id', 'position',)

        indexes = [HashIndex(fields=['item']),
                   models.Index(fields=['element'])
                   ]
