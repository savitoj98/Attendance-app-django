import csv
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Teacher, Student, School, Attendance
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import UserForm, TeacherForm, StudentForm, AttendanceForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.formsets import formset_factory
from django.utils.timezone import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User

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
        # email = form.cleaned_data['email']
        password1 = form.cleaned_data['password1']
        user.set_password(password1)
        user.save()
        Teacher.objects.create(user=user)
        user = authenticate(username=username, password=password1)
        if user is not None:
            if user.is_active:
                login(request, user)
                teachers = get_object_or_404(Teacher, user=user)
                # return render(request, 'attendance/update_page.html',{'teacher':teachers})
                return redirect('attendance:profile_update',pk=teachers.pk)
    context = {
         "form": form,
    }
    return render(request, 'attendance/register.html', context)


def login_user(request):
    if request.method == "POST":
        user_type = request.POST['user_type']
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user_type == 'Login As Teacher':
                    teachers = get_object_or_404(Teacher, user=user)
                    # students = Student.objects.filter(student_teacher=teachers)
                    # return render(request, 'attendance/profile.html',{'teacher':teachers, 'students':students})
                    return redirect('attendance:profile', pk=teachers.pk)
                elif user_type == 'Login As Principal':
                    school = get_object_or_404(School, principal=user)
                    # teachers = Teacher.objects.filter(teacher_school=school)
                    return redirect('attendance:school_detail', pk=school.pk)
            else:
                return render(request, 'attendance/login.html', {'error':'Your Account has been disabled'})
        else:
            return render(request, 'attendance/login.html', {'error_message': 'Invalid login'})
    return render(request, 'attendance/login.html',{})


def logout_user(request):
    logout(request)
    return redirect('attendance:index')


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

    def get_queryset(self):
        queryset = Teacher.objects.filter(user=self.request.user)
        test_queryset = School.objects.filter(principal=self.request.user)
        if queryset:
            return queryset
        elif test_queryset:
            queryset = Teacher.objects.filter(teacher_school=test_queryset)
            return queryset
        else:
            return queryset

class TeacherUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'attendance/profile_form.html'
    model = Teacher
    form_class = TeacherForm
    login_url = '/login/'

    def get_queryset(self):
        queryset = Teacher.objects.filter(user=self.request.user)
        return queryset

class StudentDetailView(LoginRequiredMixin,DetailView):
    template_name = 'attendance/student_detail.html'
    model = Student
    login_url = '/login/'

    def get_queryset(self):
        test_queryset = Teacher.objects.filter(user=self.request.user)
        if test_queryset:
            return Student.objects.filter(student_teacher=test_queryset)
        test_queryset2 = School.objects.filter(principal=self.request.user)
        test_queryset = Teacher.objects.filter(teacher_school=test_queryset2)
        if test_queryset:
            return Student.objects.filter(student_teacher=test_queryset)


class SchoolDetailView(LoginRequiredMixin, DetailView):
    template_name = 'attendance/school_detail.html'
    model = School
    context_object_name = 'school'

    def get_context_data(self, **kwargs):
        context = super(SchoolDetailView, self).get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.filter(teacher_school=context['school'])
        context['attendance']= Attendance.objects.filter(date=datetime.today()).filter(teacher__in=context['teachers'])
        context['students']=Student.objects.filter(student_teacher__in=context['teachers'])
        return context


@login_required
def export_to_csv(request, pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report-{}.csv"'.format(datetime.today().date())
    writer = csv.writer(response)
    writer.writerow(['Class', 'Section', 'Boys(Present)', 'Boys(Absent)', 'Girls(Present)', 'Girls(Absent)', 'Total(Present)', 'Total(Absent)' ])

    #Data For Report
    school = School.objects.filter(pk=pk)
    teachers = Teacher.objects.filter(teacher_school__in=school)
    attendance = Attendance.objects.filter(date=datetime.today()).filter(teacher__in=teachers)
    students=Student.objects.filter(student_teacher__in=teachers)
    
    #Data Writing
    for teacher in teachers:
        row = []
        st = students.filter(student_teacher=teacher)
        stMen = st.filter(student_gender='Male')
        stFemale = st.filter(student_gender='Female')
        boy = attendance.filter(student__in=stMen)
        girl = attendance.filter(student__in=stFemale)
        row.append(teacher.teacher_class)
        row.append(teacher.teacher_section)
        row.append(boy.filter(mark_attendance='Present').count())
        row.append(boy.filter(mark_attendance='Absent').count())
        row.append(girl.filter(mark_attendance='Present').count())
        row.append(girl.filter(mark_attendance='Absent').count())
        row.append(boy.filter(mark_attendance='Present').count() + girl.filter(mark_attendance='Present').count())
        row.append(boy.filter(mark_attendance='Absent').count() + girl.filter(mark_attendance='Absent').count())
        writer.writerow(row)
    return response

@login_required
def attendance_report(request, pk):

    school = School.objects.filter(pk=pk)
    if not request.user.is_authenticated():
        return redirect('attendance:login_user')
    elif school[0].principal == request.user:
        teachers = Teacher.objects.filter(teacher_school__in=school)
        date = datetime.today().date()
        attendance = Attendance.objects.filter(date=datetime.today(),teacher__in=teachers)
        students=Student.objects.filter(student_teacher__in=teachers)
        
        #For overview report
        studentMen = students.filter(student_gender='Male')
        studentFemale = students.filter(student_gender='Female')
        boys = attendance.filter(student__in=studentMen)
        girls = attendance.filter(student__in=studentFemale)
        p_boys = boys.filter(mark_attendance='Present')
        p_girls = girls.filter(mark_attendance='Present')
        a_boys = boys.filter(mark_attendance='Absent')
        a_girls = girls.filter(mark_attendance='Absent')

        #For detailed report
        boys_present = []
        girls_present = []
        boys_absent = []
        girls_absent = []
        total_present = []
        total_absent = []
        student_data = []
        for teacher in teachers:
            st = students.filter(student_teacher=teacher)
            student_data.append(st)
            stMen = st.filter(student_gender='Male')
            stFemale = st.filter(student_gender='Female')
            boy = attendance.filter(student__in=stMen)
            girl = attendance.filter(student__in=stFemale)
            boys_present.append(boy.filter(mark_attendance='Present').count())
            girls_present.append(girl.filter(mark_attendance='Present').count())
            boys_absent.append(boy.filter(mark_attendance='Absent').count())
            girls_absent.append(girl.filter(mark_attendance='Absent').count())
            total_present.append(boy.filter(mark_attendance='Present').count() + girl.filter(mark_attendance='Present').count())
            total_absent.append(boy.filter(mark_attendance='Absent').count() + girl.filter(mark_attendance='Absent').count())
        
        report_data = zip(teachers,boys_present,boys_absent,girls_present,girls_absent,total_present,total_absent,student_data)
        
        context = {
            'date':date,
            'school':school,
            'teachers':teachers,
            'attendance':attendance,          
            'p_boys':p_boys,
            'a_boys':a_boys,
            'p_girls':p_girls,
            'a_girls':a_girls,
            'report_data':report_data,
        }
        return render(request,'attendance/principal_report.html',context)
    else:
        return redirect('attendance:school_detail', pk=pk)


@login_required
def create_student(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if not request.user.is_authenticated():
        return redirect('attendance:login_user')
    elif teacher.user == request.user:
        form = StudentForm(request.POST or None, request.FILES or None)
        teacher = get_object_or_404(Teacher, pk=pk)
        students = Student.objects.filter(student_teacher=teacher)
        if form.is_valid():
            student = form.save(commit=False)
            student.student_teacher = teacher
            student.save()
            # return render(request, 'attendance/profile.html', {'teacher':teacher,'students':students})
            return  redirect('attendance:profile',pk=teacher.pk)
        context = {
            'teacher':teacher,
            'form':form,
        }
        return render(request, 'attendance/student_create.html', context)
    else:
        return HttpResponse(status=403)

@login_required
def mark_attendance(request,pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    students = Student.objects.filter(student_teacher=teacher)
    count = students.count()
    attendance_formset = formset_factory(AttendanceForm, extra=count)
    date = datetime.today().date().strftime('%d-%m-%Y')


    if not request.user.is_authenticated():
        return redirect('attendance:login_user')

    elif teacher.user == request.user:
        if request.method == 'POST':
            formset = attendance_formset(request.POST)
            list = zip(students,formset)

            if formset.is_valid():
                for form, student in zip(formset,students):
                    date = datetime.today()
                    mark = form.cleaned_data['mark_attendance']
                    print(mark)
                    check_attendance = Attendance.objects.filter(teacher=teacher,date=date,student=student)
                    print(check_attendance)
     
                    if check_attendance:
                        attendance = Attendance.objects.get(teacher=teacher,date=date,student=student)
                        if attendance.mark_attendance == 'Absent':
                            student.absent = student.absent - 1
                        elif attendance.mark_attendance == 'Present':
                            student.present = student.present - 1
                        attendance.mark_attendance = mark
                        attendance.save()

                    else: 
                        attendance = Attendance()
                        attendance.teacher = teacher
                        attendance.student = student
                        attendance.date = date
                        attendance.mark_attendance = mark
                        attendance.save()

                    if mark == 'Absent':
                        student.absent = student.absent + 1
                    if mark == 'Present':
                        student.present = student.present + 1
                    student.save()


                context = {
                    'students': students,
                    'teacher': teacher,
                }
                # return render(request, 'attendance/profile.html', context)
                return redirect('attendance:profile', pk=teacher.pk)
            else:
                error = "Something went wrong"
                context = {
                    'error': error,
                    'formset': formset,
                    'students': students,
                    'teacher': teacher,
                    'list': list,
                    'date':date,
                }
                return render(request, 'attendance/attendance_form.html', context)

        else:
            list = zip(students, attendance_formset())
            context = {
                'formset': attendance_formset(),
                'students': students,
                'teacher': teacher,
                'list': list,
                'date':date,
            }

            return render(request, 'attendance/attendance_form.html', context)

    else:
        return HttpResponse(status=403)