from rest_framework import serializers

from core.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the Tags Model"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create a new tag and return it"""
        return Tag.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update an existing tags instance and return it"""
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
