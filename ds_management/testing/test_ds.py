from django.test import TestCase
from ds_management.models import Item, ItemElement, ItemCategory, AVLTree
from django.contrib.auth.models import User
from ds_management.models import StackQueue
# from ds_management.ds_models.stack_queue_ds import StackQueueDs
# from ds_management.ds_models.item_element_ds import ItemElemenDS
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
        item_category_queue: ItemCategory = ItemCategory.objects.create(category_name='avltree')

    # def test_create_element(self):
    #     global OWNER
    #     item_category_list: ItemCategory = ItemCategory.objects.get(category_name=DataStructures.list)
    #
    #     element: Item = Item.objects.create(item_name=dummy_object_name,
    #                                         category_name=item_category_list,
    #                                         owner=OWNER
    #                                         )
    #     element_id: int = element.id
    #     recieved_element: Item = Item.objects.get(id=element_id)
    #     assert recieved_element.item_name == dummy_object_name
    #     assert recieved_element.category_name.category_name == 'list'
    #
    # def test_stack(self):
    #     global OWNER
    #     item_category_list: ItemCategory = ItemCategory.objects.get(category_name=DataStructures.stack)
    #     item: Item = Item.objects.create(item_name=dummy_object_name,
    #                                      category_name=item_category_list,
    #                                      owner=OWNER)
    #
    #     StackQueue.objects.push(item.id,
    #                                         element_data={"st": 1},
    #
    #                                         )
    #
    #     StackQueue.objects.push(item.id,
    #                                         element_data={"st": 2},
    #                                         )
    #
    #     pop_responce: Item = StackQueue.objects.pop(item.id, category="stack")
    #
    #     assert pop_responce.element_data['st'] == 2
    #
    # def test_list(self):
    #     global OWNER
    #     item_category_list: ItemCategory = ItemCategory.objects.get(category_name=DataStructures.list)
    #     item: Item = Item.objects.create(item_name=dummy_object_name,
    #                                      category_name=item_category_list,
    #                                      owner=OWNER)
    #
    #     StackQueue.objects.push(item.id,
    #                                         element_data={"st": 1},
    #                                         )
    #
    #     StackQueue.objects.push(item.id,
    #                                         element_data={"st": 2},
    #                                         )
    #
    #     pop_responce: ItemElement = StackQueue.objects.pop(item.id,category='list')
    #
    #     assert pop_responce.element_data['st'] == 1
    #
    # def test_queue(self):
    #     global OWNER
    #     item_category_queue: ItemCategory = ItemCategory.objects.get(category_name=DataStructures.queue)
    #     item: Item = Item.objects.create(item_name=dummy_object_name,
    #                                      category_name=item_category_queue,
    #                                      owner=OWNER)
    #
    #     StackQueue.objects.push(item.id,
    #                                         element_data={"st": 1},
    #                                         )
    #
    #     StackQueue.objects.push(item.id,
    #                                         element_data={"st": 2},
    #                                         )
    #
    #     pop_responce: Item = StackQueue.objects.pop(item.id,category='queue')
    #
    #     assert pop_responce.element_data['st'] == 1

    def test_avltree(self):
        global OWNER
        item_category_queue: ItemCategory = ItemCategory.objects.get(category_name=DataStructures.avltree)
        item: Item = Item.objects.create(item_name=dummy_object_name,
                                         category_name=item_category_queue,
                                         owner=OWNER)

        root = None
        tree_root = AVLTree.objects.insert(
                                      10,
                                      item.id,
                                      element_data={"st": 1},
                                      )



        root=AVLTree.objects.insert(

                               key=20,
                               item_id=item.id,
            element_data ={"st": 2},
                               )
        AVLTree.objects.insert(

            key=30,
            item_id=item.id,
            element_data={"st": 3},
        )

        AVLTree.objects.insert(

            key=40,
            item_id=item.id,
            element_data={"st": 4},
        )

        AVLTree.objects.insert(

            key=50,
            item_id=item.id,
            element_data={"st": 5},
        )

        AVLTree.objects.insert(

            key=25,
            item_id=item.id,
            element_data={"st": 3},
        )
        root = AVLTree.objects.get_root(item_id=item.id)


        result = AVLTree.objects.preOrderAsJson(root=root)
        result = AVLTree.objects.preOrder(root=root)

        assert result == [30, 20, 10, 25, 40, 50]


