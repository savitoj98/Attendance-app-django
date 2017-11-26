from django import template

register = template.Library()

@register.filter
def find_attendance(attendance,student):
    attend = attendance.filter(student=student)
    return attend[0].mark_attendance