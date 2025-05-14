from django.db import models

# Create your models here.
class Mentor(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    mode = models.CharField(max_length=50)  # e.g., 'Online', 'Meet in Person'
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    avatar = models.ImageField(upload_to='mentors/', default='default.png')

    def __str__(self):
        return self.name