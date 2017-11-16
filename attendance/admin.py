from django.contrib import admin
from .models import Student, Teacher, School, Attendance
# Register your models here.

admin.site.register(Student)
admin.site.register(School)
# admin.site.register(Attendance)

# class TeacherProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'teacher_name', 'teacher_class', 'teacher_section', 'teacher_school']

class AttendanceProfileAdmin(admin.ModelAdmin):
    list_display = ['student','teacher','date','mark_attendance']

admin.site.register(Teacher)
admin.site.register(Attendance, AttendanceProfileAdmin)