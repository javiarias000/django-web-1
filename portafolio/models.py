from django.db import models

class Technology(models.Model):
    name = models.CharField(max_length=50)
    icon_class = models.CharField(max_length=50, help_text="Tailwind o FontAwesome icon class")
    category = models.CharField(max_length=50, choices=[('FE', 'Frontend'), ('BE', 'Backend'), ('DO', 'DevOps')])

    def __str__(self):
        return self.name

from django.db import models
from parler.models import TranslatableModel, TranslatedFields

class Technology(models.Model):
    name = models.CharField(max_length=50)
    icon_class = models.CharField(max_length=50, help_text="Tailwind o FontAwesome icon class")
    category = models.CharField(max_length=50, choices=[('FE', 'Frontend'), ('BE', 'Backend'), ('DO', 'DevOps')])

    def __str__(self):
        return self.name

class Project(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=200),
        description = models.TextField()
    )
    slug = models.SlugField(unique=True)
    github_url = models.URLField()
    live_demo = models.URLField(blank=True)
    technologies = models.ManyToManyField(Technology)
    stars = models.IntegerField(default=0)  # Actualizado vía API
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()

    class Meta:
        ordering = ['-start_date']

class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()

    class Meta:
        ordering = ['-start_date']
