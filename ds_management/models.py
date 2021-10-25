from django.db import models
from django.contrib.postgres.indexes import HashIndex
from ds_management.string_constraints.string_constraints import *
from ds_management.ds_models.stack_queue_ds import StackQueueManager
from ds_management.ds_models.avltree_ds import AVLtreeManager
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


class StackQueue(ItemElement):
    position = models.IntegerField()
    objects = StackQueueManager()
    item_field = models.ForeignKey(
        Item,
        related_name='item_no',
        on_delete=models.CASCADE,
        default = ''
        )



    class Meta:
        unique_together = ('item_field', 'position',)

        indexes = [HashIndex(fields=['item_field']),

                   ]


class AVLTree(ItemElement):
    objects = AVLtreeManager()
    val = models.IntegerField(blank=True,null=True)
    root = models.BooleanField(blank=True, default=False)
    right = models.IntegerField(blank=True,null=True)
    left = models.IntegerField(blank=True,null=True)
    height = models.IntegerField(blank=True,default=1)
    item_field = models.ForeignKey(
        Item,
        related_name='item_field',
        on_delete=models.CASCADE,
        default=''
    )

    class Meta:
        # unique_together = ('item_field', 'val',)
        indexes = [HashIndex(fields=['item_field']),

                   ]

