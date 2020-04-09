from rest_framework import serializers
from .models import Question
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'slug']


#JSONRenderer().render(serializer.data)
# if __name__ == '__main__':
#     subject = Question.objects.latest('id')
#     serializer = QuestionSerializer(subject)
#     print(serializer.data)