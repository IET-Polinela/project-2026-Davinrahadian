from django.db import models


class Report(models.Model):
    STATUS_CHOICES = [
        ('REPORTED', 'Reported'),
        ('VERIFIED', 'Verified'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    CATEGORY_CHOICES = [
        ('Jalan Rusak', 'Jalan Rusak'),
        ('Sampah', 'Sampah'),
        ('Lampu Mati', 'Lampu Mati'),
        ('Drainase', 'Drainase'),
        ('Keamanan', 'Keamanan'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Jalan Rusak',
    )
    location = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='REPORTED',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
