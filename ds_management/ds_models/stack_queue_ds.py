from django.db.models import Max, Min
from ds_management.string_constraints.string_constraints import *
from ds_management.utilities import data_layer_utils
from copy import deepcopy
from django.db import models


class StackQueueManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()

    def push(self, item_id, element_data):
        """
        push new element for item:
        create new one
        :param item_id:
        :param element_id:
        :return:
        """

        if not self.get_queryset().filter(item_id=item_id).exists():
            position = 0

        else:
            element_to_push_index: int = self.get_queryset().filter(item_id=item_id).aggregate(Max(position_str))[
                'position__max']
            new_index: int = element_to_push_index + 1
            position = new_index
        new_element = self.create(item_id=item_id,
                                  position=position,
                                  element_data=element_data,
                                  item_field_id=item_id)

        return new_element

    # todo to implement as linked list:https://isaaccomputerscience.org/concepts/dsa_datastruct_stack?examBoard=all&stage=all

    def pop(self, item_id, category, remove_item=True):

        stack_queue_element_to_pop_position = None
        if self.get_queryset().filter(item_id=item_id).exists():
            if category == DataStructures.stack:
                stack_queue_element_to_pop_position: int = \
                self.get_queryset().filter(item_id=item_id).aggregate(Max(position_str))['position__max']
            elif category in [DataStructures.queue, DataStructures.list]:
                stack_queue_element_to_pop_position: int = \
                self.get_queryset().filter(item_id=item_id).aggregate(Min(position_str))['position__min']
            stack_queue_element_to_pop = self.get_queryset().get(position=stack_queue_element_to_pop_position,
                                                                 item_field=item_id)
            new_instance = deepcopy(stack_queue_element_to_pop)
            if remove_item:
                stack_queue_element_to_pop.delete()

            return new_instance

    # todo to implement as linked list:https://isaaccomputerscience.org/concepts/dsa_datastruct_stack?examBoard=all&stage=all
    def is_empty(self, item_id) -> bool:
        """
        check if data structure have any element left
        :param item_id:
        :return: item element
        """
        have_items = self.filter(item_id=item_id).exists()
        return not have_items
