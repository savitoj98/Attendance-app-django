from django.contrib import admin
from .models import Student, Teacher, School
# Register your models here.

admin.site.register(Student)
admin.site.register(School)
# admin.site.register(Attendance)

class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'teacher_name', 'teacher_class', 'teacher_section', 'teacher_school']

admin.site.register(Teacher, TeacherProfileAdmin)