from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Teacher, Student, School
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .forms import UserForm, TeacherForm, StudentForm, AttendanceForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.formsets import formset_factory

# Create your views here.

def index(request):
    return render(request, 'attendance/index.html',{})

def AboutView(request):
    return render(request, 'attendance/about.html', {})

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password1 = form.cleaned_data['password1']
        user.set_password(password1)
        user.save()
        Teacher.objects.create(user=user)
        user = authenticate(username=username,email=email, password=password1)
        if user is not None:
            if user.is_active:
                login(request, user)
                teachers = get_object_or_404(Teacher, user=user)
                return render(request, 'attendance/update_page.html',{'teacher':teachers})
    context = {
         "form": form,
    }
    return render(request, 'attendance/register.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                teachers = get_object_or_404(Teacher, user=user)
                students = Student.objects.filter(student_teacher=teachers)
                return render(request, 'attendance/profile.html',{'teacher':teachers, 'students':students})
            else:
                return render(request, 'attendance/login.html', {'error':'Your Account has been disabled'})
        else:
            return render(request, 'attendance/login.html', {'error_message': 'Invalid login'})
    return render(request, 'attendance/login.html',{})


def logout_user(request):
    logout(request)
    return render(request, 'attendance/index.html', {})


class SchoolListView(ListView):
    template_name = 'attendance/school_list.html'
    context_object_name = 'school_list'
    def get_queryset(self):
        return School.objects.all()

# def TeacherDetail(request, pk):
#     teacher = Teacher.objects.filter(pk=pk)
#     students = Student.objects.filter(student_teacher=teacher)
#     context = {
#         'teacher':teacher,
#         'students':students
#     }
#     return render(request, 'attendance/profile.html', context)


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'attendance/profile.html'

    def get_context_data(self, **kwargs):
        context = super(TeacherDetailView, self).get_context_data(**kwargs)
        context['students'] = Student.objects.filter(student_teacher=context['teacher'])
        # context['teacher'] = Student.objects.all()
        return context

class TeacherUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'attendance/profile_form.html'
    model = Teacher
    form_class = TeacherForm
    login_url = '/login/'

class StudentDetailView(LoginRequiredMixin,DetailView):
    template_name = 'attendance/student_detail.html'
    model = Student
    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        context['teacher'] = Teacher.objects.all()
        # context['teacher'] = Student.objects.all()
        return context

@login_required
def create_student(request, pk):
    if not request.user.is_authenticated():
        return render(request, 'attendance/login.html',{})
    else:
        form = StudentForm(request.POST or None, request.FILES or None)
        teacher = get_object_or_404(Teacher, pk=pk)
        students = Student.objects.filter(student_teacher=teacher)
        if form.is_valid():
            student = form.save(commit=False)
            student.student_teacher = teacher
            student.save()
            return render(request, 'attendance/profile.html', {'teacher':teacher,'students':students})
        context = {
            'teacher':teacher,
            'form':form,
        }
        return render(request, 'attendance/student_create.html', context)

@login_required
def mark_attendance(request,pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    students = Student.objects.filter(student_teacher=teacher)
    count = students.count()
    AttendanceFormSet = formset_factory(AttendanceForm, extra=count)

    if request.method == 'POST':
        formset = AttendanceFormSet(request.POST)
        list = zip(students,formset)
        if formset.is_valid():
            for form, student in zip(formset,students):
                mark = form.cleaned_data['mark_attendance']
                print(mark)
                if mark == 'Absent':
                    student.absent = student.absent + 1
                if mark == 'Present':
                    student.present = student.present + 1
                student.save()
            context = {
                'students': students,
                'teacher': teacher,
            }
            return render(request, 'attendance/profile.html', context)
        else:
            error = "Something went wrong"
            return render(request, 'attendance/attendance_form.html', {'error':error, 'formset':formset, 'students':students, 'teacher':teacher, 'list':list})

    else:
        list = zip(students, AttendanceFormSet())
        return render(request, 'attendance/attendance_form.html', {'formset':AttendanceFormSet(), 'students':students, 'teacher':teacher, 'list':list})