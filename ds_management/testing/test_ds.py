from django.test import TestCase
from ds_management.models import Item,ItemElement,ItemCategory,StackQueue
from ds_management.string_constraints.string_constraints import *
dummy_object_name = "test"
dummy_stack_data = {"st":1}
class DsTestCase(TestCase):
    def setUp(self):
        item_category_list = ItemCategory.objects.create(category_name='list')
        item_category_stack = ItemCategory.objects.create(category_name='stack')
        item_category_queue = ItemCategory.objects.create(category_name='queue')




    def test_create_element(self):

        item_category_list = ItemCategory.objects.get(category_name =DataStructures.list)

        element = Item.objects.create(item_name=dummy_object_name,
                                      category_name=item_category_list)
        element_id =element.id
        recieved_element = Item.objects.get(id = element_id)
        assert recieved_element.item_name == dummy_object_name
        assert recieved_element.category_name.category_name == 'list'

    def test_stack(self):
        item_category_list = ItemCategory.objects.get(category_name=DataStructures.stack)
        item = Item.objects.create(item_name=dummy_object_name,
                                      category_name=item_category_list)

        ItemElement.objects.add_new_element(item.id,
                                                              element_data={"st": 1},
                                                              )

        ItemElement.objects.add_new_element(item.id,
                                                              element_data={"st": 2},
                                                              )

        pop_responce = ItemElement.objects.pop(item.id)

        assert pop_responce.element_data['st'] == 2

    def test_list(self):
        item_category_list = ItemCategory.objects.get(category_name=DataStructures.list)
        item = Item.objects.create(item_name=dummy_object_name,
                                   category_name=item_category_list)

        ItemElement.objects.add_new_element(item.id,
                                            element_data={"st": 1},
                                            )

        ItemElement.objects.add_new_element(item.id,
                                            element_data={"st": 2},
                                            )

        pop_responce = ItemElement.objects.pop(item.id)

        assert pop_responce.element_data['st'] == 1

    def test_queue(self):
        item_category_list = ItemCategory.objects.get(category_name=DataStructures.queue)
        item = Item.objects.create(item_name=dummy_object_name,
                                   category_name=item_category_list)

        ItemElement.objects.add_new_element(item.id,
                                            element_data={"st": 1},
                                            )

        ItemElement.objects.add_new_element(item.id,
                                            element_data={"st": 2},
                                            )

        pop_responce = ItemElement.objects.pop(item.id)

        assert pop_responce.element_data['st'] == 1