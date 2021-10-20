from django.test import TestCase
from ds_management.models import Item, ItemElement, ItemCategory
from django.contrib.auth.models import User
from ds_management.ds_models.stack_queue_ds import StackQueueDs
from ds_management.ds_models.item_element_ds import ItemElemenDS
from ds_management.string_constraints.string_constraints import *

dummy_object_name: str = "test"
dummy_stack_data: str = {"st": 1}
test_user = 'chenlev'
OWNER = None


class DsTestCase(TestCase):
    def setUp(self):
        global OWNER
        OWNER = User.objects.create_user('foo', password='bar')
        item_category_list: ItemCategory = ItemCategory.objects.create(category_name='list')
        item_category_stack: ItemCategory = ItemCategory.objects.create(category_name='stack')
        item_category_queue: ItemCategory = ItemCategory.objects.create(category_name='queue')

    def test_create_element(self):
        global OWNER
        item_category_list: ItemCategory = ItemCategory.objects.get(category_name=DataStructures.list)

        element: Item = Item.objects.create(item_name=dummy_object_name,
                                            category_name=item_category_list,
                                            owner=OWNER
                                            )
        element_id: int = element.id
        recieved_element: Item = Item.objects.get(id=element_id)
        assert recieved_element.item_name == dummy_object_name
        assert recieved_element.category_name.category_name == 'list'

    def test_stack(self):
        global OWNER
        item_category_list: ItemCategory = ItemCategory.objects.get(category_name=DataStructures.stack)
        item: Item = Item.objects.create(item_name=dummy_object_name,
                                         category_name=item_category_list,
                                         owner=OWNER)

        ItemElemenDS.push(item.id,
                                            element_data={"st": 1},
                                            )

        ItemElemenDS.push(item.id,
                                            element_data={"st": 2},
                                            )

        pop_responce: Item = ItemElemenDS.pop(item.id)

        assert pop_responce.element_data['st'] == 2

    def test_list(self):
        global OWNER
        item_category_list: ItemCategory = ItemCategory.objects.get(category_name=DataStructures.list)
        item: Item = Item.objects.create(item_name=dummy_object_name,
                                         category_name=item_category_list,
                                         owner=OWNER)

        ItemElemenDS.push(item.id,
                                            element_data={"st": 1},
                                            )

        ItemElemenDS.push(item.id,
                                            element_data={"st": 2},
                                            )

        pop_responce: ItemElement = ItemElemenDS.pop(item.id)

        assert pop_responce.element_data['st'] == 1

    def test_queue(self):
        global OWNER
        item_category_queue: ItemCategory = ItemCategory.objects.get(category_name=DataStructures.queue)
        item: Item = Item.objects.create(item_name=dummy_object_name,
                                         category_name=item_category_queue,
                                         owner=OWNER)

        ItemElemenDS.push(item.id,
                                            element_data={"st": 1},
                                            )

        ItemElemenDS.push(item.id,
                                            element_data={"st": 2},
                                            )

        pop_responce: Item = ItemElemenDS.pop(item.id)

        assert pop_responce.element_data['st'] == 1
