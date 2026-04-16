from django.db import models   # 🔥 INI WAJIB ADA

class Report(models.Model):

    STATUS_CHOICES = [
        ('REPORTED', 'Reported'),
        ('VERIFIED', 'Verified'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]


    title = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    
    description = models.TextField()


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='REPORTED'
    )
\

def __str__(self):
        return self.title