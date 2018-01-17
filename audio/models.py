from django.db import models
from django.contrib.auth import get_user_model
from django_celery_results.models import TaskResult
import os

class Audio(models.Model):
    upload = models.FileField(upload_to='upload/', max_length=1024, null=True, blank=True)
    #XXX need to take extra steps in upload to trim filename if necessary

    source = models.URLField(blank=True, null=True, unique=True)
    uploader = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT # A user can only be destroyed if it has none.
    )

    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    processed = models.BooleanField(default=False)
    task = models.OneToOneField(
        TaskResult,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        try:
            return os.path.basename(self.upload.path)
        except ValueError:
            return str(self.source)

    @property
    def is_orphan(self):
        fields = [
            #https://docs.djangoproject.com/en/2.0/ref/models/meta/#retrieving-a-single-field-instance-of-a-model-by-name
        ]
