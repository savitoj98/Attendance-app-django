from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import Teacher,Student


class_attendance = (
    ('Present','Present'),
    ('Absent','Absent'),
)


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    class Meta:
        model = User
        fields = ['username','email','password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = ['teacher_name', 'teacher_school', 'teacher_class', 'teacher_section']
    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['student_name', 'roll_no', 'student_gender']
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class AttendanceForm(forms.Form):
    mark_attendance = forms.ChoiceField(widget=forms.RadioSelect, choices=class_attendance)