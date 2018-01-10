from django.db import models
from django.contrib.auth import get_user_model
from django_celery_results.models import TaskResult

class Audio(models.Model):
    upload = models.FileField(upload_to='upload/', max_length=1024, null=True)
    #XXX need to take extra steps in upload to trim filename if necessary

    up_from = models.URLField(null=True, unique=True)
    up_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT # A user can only be destroyed if it has none.
    )

    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    processed = models.BooleanField(default=False)
    task = models.ForeignKey(TaskResult, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        if self.upload is not None:
            return os.path.basename(self.upload.path)
        else:
            return str(self.up_from)

    CONTENT_RELATED_FIELDS = ['song',] #XXX Bad app encapsulation Create your models here.
