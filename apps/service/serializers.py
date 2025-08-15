from rest_framework import serializers
from .models import File, Service, Comment

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'images']
        read_only_fields = ['images']

class ServicesSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True, source='file_set')
    
    class Meta:
        model = Service
        fields = ['id', 'name', 'synopsis', 'description', 'create_time', 'files']
        read_only_fields = ['slug', 'create_time']

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'