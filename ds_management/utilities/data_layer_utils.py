from ds_management.models import Item,ItemCategory,ItemElement,StackQueue
from ds_management.string_constraints.string_constraints import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max


def add_element_to_stack_queue( item_id, element_id):
    if not StackQueue.objects.filter(item_id=item_id).exists():
        new_element = StackQueue.objects.create(item_id=item_id,
                                                element_id=element_id,
                                                position=0
                                                )
        return new_element

    max_position_query_result = StackQueue.objects.filter(item_id=item_id).aggregate(Max(position_str))
    new_max_position = max_position_query_result[position__max_str] + 1
    new_element = StackQueue.objects.create(item_id=item_id,
                                            element_id=element_id,
                                            position=new_max_position
                                            )

    return new_element