from rest_framework import viewsets
from typing import Dict
from rest_framework.permissions import IsAuthenticated
from ds_management.models import Item, ItemCategory, ItemElement, StackQueue
from ds_management.serializers import ItemCategorySerializer, ItemSerializer, StackQueueSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from ds_management.string_constraints.string_constraints import *


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def item_view(request):
    """
    add new item
    :param request:
    :return:
    """

    try:
        item_category: ItemCategory = ItemCategory.objects.get(category_name=request.data['category_name'])
    except:
        response_str: str = " No such category_exists"
        return_status: str = status.HTTP_400_BAD_REQUEST
        return Response(response_str, return_status)

    user: str = request.user
    try:
        element: Item = Item.objects.create(item_name=request.data['item_name'],
                                            category_name=item_category,
                                            owner=user
                                            )
        return_status: str = status.HTTP_201_CREATED
        response_str: str = {"element_id": element.id}
    except KeyError as e:
        response_str: str = str(e)
        return_status: str = status.HTTP_400_BAD_REQUEST

    return Response(response_str, return_status)


@api_view(['POST', 'GET'])
def item_element_view(request, pk):
    """
    add or remove new element
    on GET for stack queue and list the LAST ELEMENT gets removed
    """

    try:
        item: Item = Item.objects.get(pk=pk)
    except item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    ds_operation: str = request.query_params.get(operation_str)

    if ds_operation and ds_operation not in OPERATIONS:
        return Response(f"{operation} is not supported",
                        status=status.HTTP_404_NOT_FOUND)

    item_id: int = item.id
    try:
        if request.method == 'POST':
            element_data: Dict = request.data[element_data_str]
            response_result: ItemElement = ItemElement.objects.add_new_element(item_id,
                                                                               element_data,
                                                                               )
            response_data: Dict = {"element_id": response_result.id, "item_id": pk}
            result_status: str = status.HTTP_201_CREATED

        if request.method == 'GET':
            if ds_operation == OPERATIONS[peek_str]:
                response_result: ItemElement = ItemElement.objects.peek(item_id)
            else:
                response_result: ItemElement = ItemElement.objects.pop(item_id)

            if response_result:
                response_data = {
                    "item_id": pk,
                    "element_data": response_result.element_data,
                    "element_id": response_result.id
                }
                result_status: str = status.HTTP_200_OK
            else:
                response_data: str = "This item does not have elements"
                result_status: str = status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        response_data: str = str(e)
        result_status: status = status.HTTP_400_BAD_REQUEST

    return Response(response_data, status=result_status)


class ItemViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

