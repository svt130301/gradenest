from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
from .models import QuestionPaper, TimeTable
from program_management.models import Program
from accounts.models import UserProfile
from .forms import QuestionPaperForm, TimeTableForm

# ---------------------------
# Teacher/HOD Upload Question Paper
# ---------------------------
@login_required
def upload_timetable(request):
    if request.method == 'POST':
        form = TimeTableForm(request.POST, request.FILES)
        if form.is_valid():
            timetable = form.save(commit=False)
            timetable.uploaded_by = request.user  # store actual user, not UserProfile
            timetable.save()
            messages.success(request, "Timetable uploaded successfully!")
            return redirect('resource_management:upload_timetable')
    else:
        form = TimeTableForm()

    timetables = TimeTable.objects.all().order_by('-uploaded_at')
    return render(request, 'resource_management/upload_timetable.html', {
        'form': form,
        'timetables': timetables,
    })



# ---------------------------
# Office Staff Upload Time Table
# ---------------------------
@login_required
def upload_question_paper(request):
    profile = request.user.userprofile

    if request.method == 'POST':
        form = QuestionPaperForm(request.POST, request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.uploaded_by = request.user  
            paper.save()
            messages.success(request, "Question paper uploaded successfully!")
            return redirect('resource_management:upload_question_paper')
    else:
        form = QuestionPaperForm()

    # Filter depending on role
    if profile.role == 'OfficeStaff':
        question_papers = QuestionPaper.objects.all()
    else:
        question_papers = QuestionPaper.objects.filter(program=profile.program)

    return render(request, 'resource_management/upload_question_paper.html', {
        'form': form,
        'question_papers': question_papers
    })


# ---------------------------
# Student View Question Papers
# ---------------------------
@login_required
def view_question_papers(request):
    profile = request.user.userprofile
    question_papers = QuestionPaper.objects.filter(program=profile.program)
    return render(request, 'resource_management/view_question_papers.html', {'question_papers': question_papers})


# ---------------------------
# Student View Timetables
# ---------------------------
@login_required
def view_timetables(request):
    profile = request.user.userprofile
    
    # Office Staff should see all timetables
    if profile.role == 'OfficeStaff':
        timetables = TimeTable.objects.all()
    else:
        timetables = TimeTable.objects.filter(program=profile.program)
    
    return render(request, 'resource_management/view_timetables.html', {'timetables': timetables})

@login_required
def student_resources(request):
    profile = request.user.userprofile
    question_papers = QuestionPaper.objects.filter(program=profile.program)
    timetables = TimeTable.objects.filter(program=profile.program)
    return render(request, 'resource_management/student_resources.html', {
        'question_papers': question_papers,
        'timetables': timetables,
    })

@login_required
def notifications(request):
    return render(request, 'resource_management/notifications.html')

def view_notifications(request):
    return render(request, 'resource_management/view_notifications.html')


