from typing import Tuple,Dict


class DataStructures:
    stack: str = "stack"
    array: str = "array"
    queue: str = "queue"
    list: str = "list"



structure_str: str = "structure"
element_data_str: str = 'element_data'
item_str: str = 'item'
item_name_str: str = 'item_name'
item_category_str: str = 'item_category'
position_str: str = 'position'
item_id_str: str = 'item_id'
position__max_str: str = 'position__max'
position__min_str: str = 'position__min'
category_str: str = 'category'
name_str: str = 'name'
operation_str: str = 'operation'
peek_str: str = 'peek'
OPERATIONS: Dict = {
    'peek' :"peek",
    'pop':  "pop",
    'push': "queue"}

LIST: str = 'L'
STACK: str = 'S'
QUEUE: str = 'Q'
STRUCTURE_CHOICES: Tuple = (
    (LIST, 'list'),
    (STACK, 'stack'),
    (QUEUE, 'queue'),
)
