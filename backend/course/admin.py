from django.contrib import admin

from .models import (
    Category,
    Course,
    Rating,
    Module,
    Lecture,
    Forum,
    LiveClass
)

# Register your models here.


class ModuleAdmin(admin.ModelAdmin):
    """Customizing Admin Interface"""
    list_display = ['title', 'course']
    list_display_links = ['title']
    list_filter = ['title']
    search_fields = ['title']


class LectureAdmin(admin.ModelAdmin):
    """Customizing Admin Interface"""
    list_display = ['title', 'module']
    list_display_links = ['title']
    list_filter = ['title']
    search_fields = ['title']


class LiveClassAdmin(admin.ModelAdmin):
    """Customizing Admin Interface"""
    list_display = ['title', 'course']
    list_display_links = ['title']
    list_filter = ['title']
    search_fields = ['title']


admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Rating)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Forum)
admin.site.register(LiveClass, LiveClassAdmin)
