from rest_framework import serializers
from .models import Question, StatCounter


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'slug']


class StatCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatCounter
        fields = '__all__'
