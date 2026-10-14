from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils import timezone
from .models import Task
from .forms import TaskForm


def dashboard(request):
    """Main dashboard view with task statistics."""
    tasks = Task.objects.all()
    total = tasks.count()
    done_count = tasks.filter(done=True).count()
    pending = total - done_count
    overdue = sum(1 for t in tasks if t.is_overdue)
    high_priority = tasks.filter(priority="H", done=False).count()

    # Category breakdown
    category_stats = (
        tasks.filter(done=False)
        .values("category")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    context = {
        "total": total,
        "done_count": done_count,
        "pending": pending,
        "overdue": overdue,
        "high_priority": high_priority,
        "category_stats": category_stats,
        "category_labels": dict(Task.CATEGORY),
    }
    return render(request, "task/dashboard.html", context)


def task_list(request):
    """List all tasks with filtering and search."""
    tasks = Task.objects.all()

    # Search
    query = request.GET.get("q", "")
    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Filter by status
    status_filter = request.GET.get("status", "")
    if status_filter:
        if status_filter == "overdue":
            tasks = [t for t in tasks if t.is_overdue]
        else:
            tasks = tasks.filter(status=status_filter)

    # Filter by priority
    priority_filter = request.GET.get("priority", "")
    if priority_filter:
        if isinstance(tasks, list):
            tasks = [t for t in tasks if t.priority == priority_filter]
        else:
            tasks = tasks.filter(priority=priority_filter)

    # Filter by category
    category_filter = request.GET.get("category", "")
    if category_filter:
        if isinstance(tasks, list):
            tasks = [t for t in tasks if t.category == category_filter]
        else:
            tasks = tasks.filter(category=category_filter)

    context = {
        "tasks": tasks,
        "query": query,
        "status_filter": status_filter,
        "priority_filter": priority_filter,
        "category_filter": category_filter,
        "status_choices": Task.STATUS,
        "priority_choices": Task.PRIORITY,
        "category_choices": Task.CATEGORY,
    }
    return render(request, "task/task_list.html", context)


def task_create(request):
    """Create a new task."""
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "task/task_form.html", {"form": form, "title": "Create Task"})


def task_edit(request, pk):
    """Edit an existing task."""
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "task/task_form.html", {"form": form, "title": "Edit Task", "task": task})


def task_delete(request, pk):
    """Delete a task."""
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect("task_list")
    return render(request, "task/task_confirm_delete.html", {"task": task})


def task_toggle(request, pk):
    """Toggle task done status via AJAX."""
    task = get_object_or_404(Task, pk=pk)
    task.done = not task.done
    if task.done:
        task.status = "done"
    else:
        task.status = "todo"
    task.save()
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"done": task.done, "status": task.status})
    return redirect("task_list")


def task_detail(request, pk):
    """View task details."""
    task = get_object_or_404(Task, pk=pk)
    return render(request, "task/task_detail.html", {"task": task})
