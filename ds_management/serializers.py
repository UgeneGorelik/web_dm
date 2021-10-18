from rest_framework import serializers
from ds_management.models import ItemCategory
from ds_management.models import Item,ItemElement,StackQueue
import ds_management.views


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = (
            'category_name',
            )


class ItemSerializer(serializers.ModelSerializer):
    item_elements = serializers.StringRelatedField(many=True)
    category_name = serializers.CharField(source="category_name.category_name", read_only=True)
    class Meta:
        model = Item
        fields = (
            'item_name',
            'category_name',
            'item_elements'

            )



class ItemElementSerializer(serializers.ModelSerializer):
    # Display the category name


    class Meta:
        model = ItemElement
        fields = (
            'element_data',
            'items',
            )

class StackQueueSerializer(serializers.HyperlinkedModelSerializer):
    item_id= serializers.SlugRelatedField(queryset=Item.objects.all(),
                                        slug_field='item')

    class Meta:
        model = StackQueue
        fields = (
            'item_id',
            'element_id',
        )
