from rest_framework import serializers
from materials.models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    number_lessons = serializers.SerializerMethodField()
    # source = 'lesson_set.all.first.name'
    lessons_name = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_name(self, obj):
        return [lesson.name for lesson in Lesson.objects.filter(course=obj)]

    def get_number_lessons(self, obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


# class CourseCreateSerializer(serializers.ModelSerializer):
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