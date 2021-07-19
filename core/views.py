from django.shortcuts import render, get_object_or_404,HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic.edit import FormMixin
import csv
from .forms import UserForm, CourseForm, DepartmentForm, StudentForm,SearchForm
from .models import Department, Course, Student, User


class HomepageView(generic.TemplateView):
    template_name = 'core/home.html'

class UserRegistrationView(SuccessMessageMixin, generic.TemplateView):
    model = User
    form_class = UserForm
    template_name = 'core/register.html'
    success_message = 'Your account has been successfully created'


    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('home')
            )
        return super().dispatch(request, *args, **kwargs)

    
    def post(self, request, *args, **kwargs):
        register_form = UserForm(self.request.POST)

        if register_form.is_valid():
            user = register_form.save(commit=True)
            messages.success(self.request, self.success_message)
            user.save()
            return HttpResponseRedirect(
                reverse_lazy('login')
            )
        return self.render_to_response(
            self.get_context_data(
                register_form=register_form
            )
        )

    def get_context_data(self, **kwargs):
        if 'register_form' not in kwargs:
            kwargs['register_form'] = UserForm
        return super().get_context_data(**kwargs)

class UserLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True

class LogoutView(generic.RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)
             


class DepartmentCreateView(LoginRequiredMixin,SuccessMessageMixin,generic.CreateView):
    form_class = DepartmentForm
    template_name = 'core/dept_mod.html'
    success_url = reverse_lazy('core:dept-list')
    success_message = 'New Department Created Successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Department'
        context['saveBtn'] = 'Add Department'
        return context


class DepartmentListView(LoginRequiredMixin,generic.ListView):
    queryset = Department.objects.all()
    template_name = 'core/dept_list.html'
    context_object_name = 'depts'

    # def post(self, request):
    #     queryset = 

class DepartmentUpdateView(LoginRequiredMixin,SuccessMessageMixin,generic.UpdateView):
    form_class = DepartmentForm
    template_name = 'core/dept_mod.html'
    success_url = reverse_lazy('core:dept-list')
    success_message = 'Department updated successfully'
    queryset = Department.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modify Department'
        context['saveBtn'] = 'Update Department'
        return context

class DepartmentDeleteView(LoginRequiredMixin,SuccessMessageMixin, generic.DeleteView):
    template_name = 'core/dept_del.html'
    success_message = 'Department has been removed successfully'
    queryset = Department.objects.all()
    success_url = reverse_lazy('core:dept-list')

    def get(self, request, pk):
        dept = get_object_or_404(Department, pk=pk)
        return render(request, self.template_name, {'dept':dept})

class CourseCreateView(LoginRequiredMixin,SuccessMessageMixin, generic.CreateView):
    template_name = 'core/course_mod.html'
    success_message = 'Course created successfully'
    success_url = reverse_lazy('core:course-list')
    form_class = CourseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Course'
        context['saveBtn'] = 'Add Course'
        return context


class CourseListView(LoginRequiredMixin,FormMixin,generic.ListView):
    template_name = 'core/course_list.html'
    queryset = Course.objects.all()
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form_class(self.request.GET)
        context['courses'] = self.queryset
        context['form'] = form
        if self.request.method == 'GET':
            if form.is_valid():
                context['courses'] = self.queryset.filter(name__icontains=form.cleaned_data['name'])

                # if form.cleaned_data['export_to_csv'] == True:
                #     def render_to_response(self, context=context['courses']):
                #         response = HttpResponse(content_type='text/csv')
                #         response['Content-Disponsition'] = 'attachement; filename="List of Courses.csv"'
                #         writer = csv.writer(response)
                #         writer.writerow(['Name', 'Department', 'Intake', 'Created', 'Code'])
                #         instance = context['courses']
                #         for course in instance:
                #             writer.writerow([course.name, course.department, course.intake, course.created, course.code])
                #         return super().render_to_response(response)
        return context
        
    

class CourseUpdateView(LoginRequiredMixin,SuccessMessageMixin, generic.UpdateView):
    form_class = CourseForm
    template_name = 'core/course_mod.html'
    success_url = reverse_lazy('core:course-list')
    success_message = 'Course updated successfully'
    queryset = Course.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modify course'
        context['saveBtn'] = 'Update'
        return context


class CourseDeleteView(LoginRequiredMixin,SuccessMessageMixin, generic.DeleteView):
    template_name = 'core/course_del.html'
    success_message = 'Course deleted successfully'
    success_url = reverse_lazy('core:course-list')
    queryset = Course.objects.all()

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        return render(request, self.template_name, {'course':course})

    


class StudentCreateView(LoginRequiredMixin,SuccessMessageMixin, generic.CreateView):
    template_name = 'core/student_mod.html'
    success_message = 'Student saved successfully'
    form_class = StudentForm
    success_url = reverse_lazy('core:student-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Student'
        context['saveBtn'] = 'Add Student'
        return context
    
    
    def form_valid(self, form):
        if form.is_valid():
            student = form.save(commit=False)
            student.department = student.course.department
            student.save()
            messages.success(self.request, self.success_message)
            return super().form_valid(form)


class StudentListView(LoginRequiredMixin,generic.ListView):
    template_name = 'core/student_list.html'
    queryset = Student.objects.all()
    context_object_name = 'students'


class StudentDetailView(LoginRequiredMixin,generic.DetailView):
    template_name = 'core/student_detail.html'
    queryset = Student.objects.all()
    context_object_name = 'student'

class StudentUpdateView(LoginRequiredMixin,SuccessMessageMixin, generic.UpdateView):
    template_name = 'core/student_mod.html'
    success_message = 'Student details updated successfully'
    form_class = StudentForm
    queryset = Student.objects.all()
    success_url = reverse_lazy('core:student-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Student Data'
        context['saveBtn'] = 'Update'
        return context

    def form_valid(self, form):
        student = form.save(commit=False)
        student.department = student.course.department
        student.save()
        messages.success(self.request, self.success_message)
        return reverse_lazy('core:student-list')

class StudentDeleteView(LoginRequiredMixin,SuccessMessageMixin, generic.DeleteView):
    template_name = 'core/student_del.html'
    success_message = 'Student Data deleted successfully'
    success_url = reverse_lazy('core:student-list')
    queryset = Student.objects.all()

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        return render(request, self.template_name, {'student':student})

