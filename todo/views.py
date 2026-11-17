from django.shortcuts import render, redirect, get_object_or_404
from .models import Task


def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'todo/task_list.html', {'tasks': tasks})


def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if title:
            Task.objects.create(
                title=title,
                description=description
            )
            return redirect('todo:task_list')

        return render(
            request,
            'todo/task_form.html',
            {'error': 'Title Cannot Be Empty.'}
        )

    return render(request, 'todo/task_form.html')


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if title:
            task.title = title
            task.description = description
            task.save()

            return redirect('todo:task_list')

        return render(
            request,
            'todo/task_form.html',
            {
                'task': task,
                'error': 'Title Cannot Be Empty.'
            }
        )

    return render(
        request,
        'todo/task_form.html',
        {'task': task}
    )


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.delete()
        return redirect('todo:task_list')

    return render(
        request,
        'todo/task_delete.html',
        {'task': task}
    )


def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.completed = not task.completed
        task.save()

    return redirect('todo:task_list')