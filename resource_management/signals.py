from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import QuestionPaper, TimeTable, ResourceNotification

# When a Question Paper is uploaded by Teacher/HOD
@receiver(post_save, sender=QuestionPaper)
def create_notification_for_questionpaper(sender, instance, created, **kwargs):
    if created:
        message = (
            f"New {instance.get_question_type_display()} question paper uploaded "
            f"for {instance.subject.name} (Sem {instance.semester})."
        )
        ResourceNotification.objects.create(
            resource_type='QUESTION_PAPER',
            message=message,
            program=instance.program,
            semester=instance.semester
        )

# When a Time Table is uploaded by Office Staff
@receiver(post_save, sender=TimeTable)
def create_notification_for_timetable(sender, instance, created, **kwargs):
    if created:
        message = (
            f"New {instance.get_exam_type_display()} timetable uploaded for "
            f"{instance.program.name} (Sem {instance.semester})."
        )
        ResourceNotification.objects.create(
            resource_type='TIMETABLE',
            message=message,
            program=instance.program,
            semester=instance.semester
        )



