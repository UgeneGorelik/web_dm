from django.db import models
from django.db.models import Max
from django.contrib.postgres.indexes import HashIndex

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
            indexes = [(HashIndex(fields=('item',)),),]




