from django import template

register = template.Library()

@register.filter
def find_attendance(attendance,student):
    attend = attendance.filter(student=student)
    if attend:
    	return attend[0].mark_attendance
    else:
    	return 'Null'