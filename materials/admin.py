from django.contrib import admin

from materials.models import Course, Lesson


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'preview', 'description', 'owner', )
    list_filter = ('name',)
    # search_fields = ('name', 'id',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'preview', 'description', 'link_to_video', 'course', 'owner',)
    list_filter = ('name',)
    # search_fields = ('name', 'id',)
