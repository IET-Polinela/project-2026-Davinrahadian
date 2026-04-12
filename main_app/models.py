from django.db import models

<<<<<<< HEAD
=======
# STATUS WORKFLOW
STATUS_CHOICES = [
    ('REPORTED', 'Reported'),
    ('VERIFIED', 'Verified'),
    ('IN_PROGRESS', 'In Progress'),
    ('RESOLVED', 'Resolved'),
]

>>>>>>> 8426490 (Labsession4)
class Report(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
<<<<<<< HEAD
    status = models.CharField(max_length=20, default='REPORTED')
=======

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='REPORTED'
    )

>>>>>>> 8426490 (Labsession4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title