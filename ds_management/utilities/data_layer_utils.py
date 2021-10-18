from ds_management.models import Item,ItemCategory,ItemElement,StackQueue
from ds_management.string_constraints.string_constraints import *
from ds_management.serializers import StackQueueSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max


def add_new_element( item_id, element_data,structure_type):

    element = ItemElement.objects.create(item_id=item_id,
                                         element_data=element_data,
                                         )


    if structure_type and structure_type is DataStructures.queue or DataStructures.stack:
        new_element = StackQueue.objects.push(item_id=item_id,
                                              element_id=element.id)
        new_element_serializer = StackQueueSerializer(new_element)
        response_data = {"id": new_element_serializer.id}
        return new_element