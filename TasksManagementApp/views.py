from django.shortcuts import render, redirect, get_object_or_404
from .forms import loginForm, registerForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import Task, Employee
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = registerForm(request.POST)
        print("valid:", form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)  # לא שומר עדיין
            password = form.cleaned_data.get('password')
            user.set_password(password)     # הצפנה מובנית של Django
            user.save()
            messages.success(request, 'Registration successful')
            return redirect('login')
    else:
        form = registerForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if(request.method == 'POST'):
        form = loginForm(request.POST)
        if(form.is_valid()):
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    print("success")
                    auth_login(request, user)
                    return redirect('tasks')
            except Exception as e:
                print("error:", e)
                messages.error(request, 'Error occurred during login')
                form = loginForm()
        else:
            messages.error(request, 'שם משתמש או סיסמה שגויים')
    else:
        form = loginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def tasks(request):
    user = request.user
    role = user.employee_role
    employees = Employee.objects.all()
    tasks_qs = get_tasks_for_current_user(request)


    # סינון
    status = request.GET.get('status')
    employee = request.GET.get('employee')
    if status:
        tasks_qs = tasks_qs.filter(task_status=status)
    if employee:
        tasks_qs = tasks_qs.filter(task_employee=employee)

    return render(request, 'tasks.html', {
        'user': user,
        'role': role,
        'tasks': tasks_qs,
        'employees': employees,
    })

@require_POST
@login_required
def add_task(request):
    if request.user.employee_role != 1:
        return redirect('tasks')
    name = request.POST.get('task_name')
    desc = request.POST.get('task_description')
    date = request.POST.get('task_last_date')
    status = request.POST.get('task_status')
    Task.objects.create(
        task_name=name,
        task_description=desc,
        task_last_date=date,
        task_status=1,
        task_team=request.user.employee_Team,
    )
    return redirect('tasks')

@require_POST
@login_required
def delete_task(request, task_id):
    if request.user.employee_role != 1:
        return redirect('tasks')
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect('tasks')

@require_POST
@login_required
def take_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if not task.task_employee:
        task.task_employee = request.user
        task.task_status = 2  # הגדרת סטטוס כבתהליך
        task.save()
    return redirect('tasks')

@require_POST
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.user.employee_role != 1:
        return redirect('tasks')
    # if request.method == 'POST':
        task.task_name = request.POST.get('task_name')
        task.task_description = request.POST.get('task_description')
        task.task_last_date = request.POST.get('task_last_date')
        task.task_status = request.POST.get('task_status')
        task.save()
        return redirect('tasks')
@require_POST
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.user == task.task_employee:
        task.task_status = 3  # הגדרת סטטוס כהושלם
        task.task_completed_date = timezone.now().date()
        task.save()
    return redirect('tasks')

def get_tasks_for_current_user(request):
    user = request.user
    team = user.employee_Team
    tasks = Task.objects.filter(task_team=team)
    return tasks
   


