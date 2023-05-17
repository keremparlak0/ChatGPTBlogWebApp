from rest_framework import serializers
from models import *



class AuthorSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Author.objects.create(**validated_data)
    def read():
        pass
    def update():
        pass
    def delete():
        pass

class DraftSerializer(serializers.Serializer):
    author = serializers.RelatedField(source='Author', read_only=True)
    title = serializers.CharField()
    content = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Draft.objects.create(**validated_data)
    
    def read():
        pass
    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance
    
    def delete():
        pass


class BlogSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Blog.objects.create(**validated_data)
    def read():
        pass
    def update():
        pass
    def delete():
        pass


class FollowSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Follow.objects.create(**validated_data)
    def read():
        pass
    def update():
        pass
    def delete():
        pass


class CommentSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Comment.objects.create(**validated_data)
    def read():
        pass
    def update():
        pass
    def delete():
        pass