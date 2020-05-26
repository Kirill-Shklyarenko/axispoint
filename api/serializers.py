from rest_framework import serializers
from axis.models import Letters


class LettersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letters
        fields = ('id', 'category', 'sender', 'title', 'text', 'date',)
        read_only_fields = ('id', 'category', 'sender', 'title', 'text', 'date',)
