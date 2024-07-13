from rest_framework import serializers

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("name_of_course", "description")


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ("name", "description")
