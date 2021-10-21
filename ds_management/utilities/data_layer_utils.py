# from ds_management.models import Item,ItemCategory,ItemElement,StackQueue
# from ds_management.string_constraints.string_constraints import *
# from ds_management.models import ItemElement,Item,StackQueue;
#
# def get_item_by_pk(item_id):
#     item: Item = Item.objects.get(pk=item_id)
#     return item
#
# def get_item_element_by_id(element_id):
#     element: ItemElement = ItemElement.objects.get(id=element_id)
#     return element
#
# def check_if_stack_queue_empty(item_id):
#     have_items = StackQueue.filter(item_id=item_id).exists()
#     return not have_items