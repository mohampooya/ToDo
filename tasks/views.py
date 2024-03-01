from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, CombinedUserProfileForm, TaskForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import TaskList, Task
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import BackgroundForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Task
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form})

@login_required
@require_POST
def toggle_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, list__user=request.user)  # Ensure task belongs to user
    task.completed = not task.completed
    task.save()
    return JsonResponse({'completed': task.completed})

from django.shortcuts import render
import percato
from .forms import UploadFileForm

def upload_and_ocr(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Assuming your form saves the uploaded file to 'uploaded_file'
            uploaded_file = request.FILES['uploaded_file']
            ocr = PerCato()
            extracted_text = ocr.image_to_string(uploaded_file)
            return render(request, 'ocr_results.html', {'extracted_text': extracted_text})
    else:
        form = UploadFileForm()
    return render(request, 'upload_form.html', {'form': form})

def view_list(request, list_id):
    task_list = get_object_or_404(TaskList, id=list_id)
    tasks = task_list.tasks.all()
    return render(request, 'task_list_detail.html', {'task_list': task_list, 'tasks': tasks})

def main_page(request):
    #placeholder
    return render(request, 'main_page.html')

@login_required
def dashboard(request):
    tasks_tasklist = TaskList.objects.filter(user=request.user)
    list_id = request.GET.get('list_id')
    today = timezone.now().date()
    daily_task_list, created = TaskList.objects.get_or_create(
        user=request.user, 
        name="Daily Task", 
        defaults={'date_created': today}
    )
    
    if list_id:
        selected_list = get_object_or_404(TaskList, id=list_id, user=request.user)
        tasks = Task.objects.filter(list_id=selected_list.id)
    else:
        tasks = Task.objects.filter(list=daily_task_list)
        selected_list = daily_task_list
    
    return render(request, 'dashboard.html', {
        'tasks_tasklist': tasks_tasklist,
        'tasks': tasks,
        'selected_list': selected_list,
    })
    if request.method == 'POST':
        form = BackgroundForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BackgroundForm(instance=request.user.userprofile)
    return render(request, 'dashboard.html', {'form': form, 'background': request.user.userprofile.background})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def forgot_password(request):
    return render(request, 'forgot_password.html')



@login_required
def create_task(request, list_id=None):  # Add list_id as an optional argument
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        task_list_id = request.POST.get('task_list')

        if task_list_id:
            task_list = get_object_or_404(TaskList, id=task_list_id, user=request.user)
            task = Task(title=title, description=description, list=task_list)
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please select a task list.')

    tasks_tasklist = TaskList.objects.filter(user=request.user)
    return render(request, 'create_task.html', {'tasks_tasklist': tasks_tasklist})

def update_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'update_task.html', {'form': form})

def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    task.delete()
    return redirect('dashboard')

def create_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        new_list = TaskList(name=name, user=request.user)
        new_list.save()
        return redirect('dashboard')
    return render(request, 'create_list.html')

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def create_or_edit_task(request, task_id=None):
    task = None
    if task_id:
        task = Task.objects.get(id=task_id)
    task_lists = TaskList.objects.all()
    if request.method == "POST":
        pass  # Handle form submission
    return render(request, 'create_task.html', {'task': task, 'task_lists': task_lists})

@login_required
def profile_customization(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'custom_background' in request.FILES:
                profile.background = request.FILES['custom_background']
            elif form.cleaned_data['background_choice'] != 'custom':
                profile.background = form.cleaned_data['background_choice']
            profile.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=request.user.userprofile)
    return render(request, 'profile_customization.html', {'form': form})
