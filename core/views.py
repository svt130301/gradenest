# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from program_management.models import Program, Subject   # ✅ use models from program_management
from program_management.forms import ProgramForm, SubjectForm


# ----------------- PROGRAM MANAGEMENT -----------------
@login_required
def program_list(request):
    programs = Program.objects.all()
    return render(request, 'program_management/program_list.html', {'programs': programs})


@login_required
def program_add(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program added successfully!')
            return redirect('program_management:program_list')
    else:
        form = ProgramForm()
    return render(request, 'program_management/program_form.html', {'form': form, 'title': 'Add Program'})


@login_required
def program_edit(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program updated successfully!')
            return redirect('program_management:program_list')
    else:
        form = ProgramForm(instance=program)
    return render(request, 'program_management/program_form.html', {'form': form, 'title': 'Edit Program'})


@login_required
def program_delete(request, pk):
    program = get_object_or_404(Program, pk=pk)
    program.delete()
    messages.success(request, 'Program deleted successfully!')
    return redirect('program_management:program_list')


# ----------------- SUBJECT MANAGEMENT -----------------
@login_required
def subject_list(request):
    subjects = Subject.objects.select_related('program').all()
    return render(request, 'program_management/subject_list.html', {'subjects': subjects})


@login_required
def subject_add(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added successfully!')
            return redirect('program_management:subject_list')
    else:
        form = SubjectForm()
    return render(request, 'program_management/subject_form.html', {'form': form, 'title': 'Add Subject'})


@login_required
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated successfully!')
            return redirect('program_management:subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'program_management/subject_form.html', {'form': form, 'title': 'Edit Subject'})


@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    subject.delete()
    messages.success(request, 'Subject deleted successfully!')
    return redirect('program_management:subject_list')

