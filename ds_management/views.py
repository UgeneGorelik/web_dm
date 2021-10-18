from rest_framework import viewsets
from ds_management.models import Item,ItemCategory,ItemElement,StackQueue
from ds_management.utilities.data_layer_utils import add_element_to_stack_queue
from ds_management.serializers import ItemCategorySerializer,ItemSerializer,ItemElementSerializer,StackQueueSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from ds_management.string_constraints.string_constraints import *


@csrf_exempt
@api_view(['POST'])
def add_item(request):
    """
    List all articles or create a new article.
    """

    item_serializer = ItemSerializer(data=request.data)
    try:
        item_category = ItemCategory.objects.get(category_name = request.data['category_name'] )
    except:
        Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if item_serializer.is_valid():
        element = Item.objects.create(item_name =request.data['item_name'],
                                      category_name=item_category,
                                             )
        return Response({"element_id":element.id}, status=status.HTTP_201_CREATED)
    return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def add_item_element(request, pk):
    """
    List all articles, or create a new article.
    """

    try:
        item = Item.objects.get(pk=pk)
    except item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    element_to_insert = request.data
    element=ItemElement.objects.create(item_id=item.id,
                               element_data=element_to_insert[element_data_str],
                               )
    structure_type = item.item_type.category_name
    if structure_type and structure_type is DataStructures.queue or DataStructures.stack:
        new_element = add_element_to_stack_queue(item_id=item.id,
                                                 element_id=element.id)
        new_element_serializer = StackQueueSerializer(new_element)

    return Response(request.data, status=status.HTTP_201_CREATED)






class ItemCategoryViewSet(viewsets.ModelViewSet):
    """
    List all workers, or create a new worker.
    """
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer


class ItemViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class StackQueueViewSet(viewsets.ModelViewSet):
    """
    List all workers, or create a new worker.
    """
    queryset = StackQueue.objects.all()
    serializer_class = StackQueueSerializer


