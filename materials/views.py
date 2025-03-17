from rest_framework import viewsets
from rest_framework import generics

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
