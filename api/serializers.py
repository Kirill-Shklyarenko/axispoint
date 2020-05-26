from rest_framework import serializers
from axis.models import Letters


class LettersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letters
        fields = '__all__'
        read_only_fields = ('id', 'category', 'sender', 'title', 'text', 'date',)
