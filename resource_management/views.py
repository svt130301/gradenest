from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from .models import QuestionPaper, TimeTable
from program_management.models import Program
from accounts.models import UserProfile
from .forms import QuestionPaperForm, TimeTableForm
import mimetypes
import os


# ---------------------------
# Upload Timetable (Office Staff)
# ---------------------------
@login_required
def upload_timetable(request):
    if request.method == 'POST':
        form = TimeTableForm(request.POST, request.FILES)
        if form.is_valid():
            timetable = form.save(commit=False)
            timetable.uploaded_by = request.user
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
# Upload Question Paper (Teacher / HOD)
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
    question_papers = QuestionPaper.objects.filter(
        program=profile.program,
        semester=getattr(profile, 'current_semester', 1)
    )
    return render(request, 'resource_management/view_question_papers.html', {
        'question_papers': question_papers
    })



# ---------------------------
# Student View Timetables (LIST VIEW)
# ---------------------------
@login_required
def view_timetables(request):
    profile = request.user.userprofile
    # Ensure semester filter is applied so only relevant timetables show
    timetables = TimeTable.objects.filter(
        program=profile.program,
        semester=getattr(profile, 'current_semester', 1)  # use 1 if not set
    ).order_by('-uploaded_at')
    return render(request, 'resource_management/view_timetables.html', {
        'timetables': timetables
    })



# ---------------------------
# View a Single Timetable File
# ---------------------------
def view_timetable_file(request, pk):
    timetable = get_object_or_404(TimeTable, pk=pk)
    file_path = timetable.file.path

    if not os.path.exists(file_path):
        raise Http404("File not found")

    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = 'application/pdf'

    try:
        response = FileResponse(open(file_path, 'rb'), content_type=mime_type)
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
        return response
    except Exception as e:
        raise Http404(f"Error opening file: {e}")


# ---------------------------
# Combined Student Resources View
# ---------------------------
@login_required
def student_resources(request):
    profile = UserProfile.objects.get(user=request.user)
    
    # Filter only for the student's program and current semester
    question_papers = QuestionPaper.objects.filter(
        program=profile.program,
        semester=profile.current_semester
    )

    timetables = TimeTable.objects.filter(
        program=profile.program,
        semester=profile.current_semester
    )

    context = {
        'question_papers': question_papers,
        'timetables': timetables,
    }

    return render(request, 'resource_management/student_resources.html', context)


# ---------------------------
# Notifications
# ---------------------------
@login_required
def notifications(request):
    return render(request, 'resource_management/notifications.html')


def view_notifications(request):
    return render(request, 'resource_management/view_notifications.html')

