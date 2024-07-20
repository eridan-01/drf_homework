from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    @staticmethod
    def get_lessons_count(obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ("title", "description", "lessons_count", "lessons")
