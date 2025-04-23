from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    created_at = serializers.CharField(read_only=True)
    updated_at = serializers.CharField(read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='link_to_video')]


class CourseSerializer(serializers.ModelSerializer):
    created_at = serializers.CharField(read_only=True)
    updated_at = serializers.CharField(read_only=True)

    number_lessons = serializers.SerializerMethodField()
    lessons_name = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_name(self, obj):
        """  """
        return [lesson.name for lesson in Lesson.objects.filter(course=obj)]

    def get_number_lessons(self, obj):
        """  """
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    # read_only=True
    created_at = serializers.CharField(read_only=True)
    owner = serializers.IntegerField(read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'


# class CourseCreateSerializer(serializers.ModelSerializer):
#     owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     lessons = LessonSerializer(many=True)
#
#     class Meta:
#         model = Course
#         fields = '__all__'
#
#     def create(self, validated_data):
#         lessons = validated_data.pop('course')
#
#         course = Course.objects.create(**validated_data)
#
#         for lesson in lessons:
#             Lesson.objects.create(**lesson, course=course)
#
#         return course
