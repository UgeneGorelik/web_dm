from rest_framework import viewsets
from ds_management.models import Item,ItemCategory,ItemElement,StackQueue
from ds_management.serializers import ItemCategorySerializer,ItemSerializer,StackQueueSerializer
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


    try:
        item_category = ItemCategory.objects.get(category_name = request.data['category_name'] )
    except:
        response_str ="No such category_exists"
        return_status = status.HTTP_400_BAD_REQUEST
        return Response(response_str, return_status)


    try:
        element = Item.objects.create(item_name =request.data['item_name'],
                                          category_name=item_category,
                                                 )
        return_status = status.HTTP_201_CREATED
        response_str = {"element_id":element.id}
    except Exception as e:
        response_str = str(e)
        return_status = status.HTTP_400_BAD_REQUEST

    return Response(response_str, return_status)



@csrf_exempt
@api_view(['POST','GET'])
def item_element(request, pk):
    """
    List all articles, or create a new article.
    """

    try:
        item = Item.objects.get(pk=pk)
    except item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    item_id =item.id
    if request.method == 'POST':

        element_data = request.data[element_data_str]
        response_result = ItemElement.objects.add_new_element(item_id,
                                                              element_data,
                                                              )
        response_data={"element_id":response_result.id,"item_id":pk}
        result_status =status.HTTP_201_CREATED

    if request.method == 'GET':
            response_result = ItemElement.objects.pop(item_id)
            if response_result:
                response_data = {
                             "item_id": pk,
                             "element_data":response_result.element_data,
                             "element_id": response_result.id
                             }
                result_status = status.HTTP_200_OK
            else:
                response_data="This item does not have elements"
                result_status= status.HTTP_400_BAD_REQUEST


    return Response(response_data, status=result_status)




@csrf_exempt
@api_view(['GET'])
def get_item_element( pk):
    """
    List all articles, or create a new article.
    """

    try:
        item = Item.objects.get(pk=pk)
    except item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    structure_type = item.category_name.category_name
    if structure_type and structure_type is DataStructures.queue or DataStructures.stack:
        new_element = StackQueue.objects.pop(item_id=item.id)
        new_element_serializer = StackQueueSerializer(new_element)

    return Response(new_element_serializer.data, status=status.HTTP_201_CREATED)






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


