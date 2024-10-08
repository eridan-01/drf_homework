from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import YouTubeLinkValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YouTubeLinkValidator(field="video_url")]


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    @staticmethod
    def get_lessons_count(obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = ("title", "description", "is_subscribed", "lessons_count", "lessons")


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
