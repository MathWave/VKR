from django.db import models


class Language(models.Model):
    name = models.TextField()
    work_name = models.TextField(default='')
    file_type = models.TextField(null=True)
    logo = models.ImageField(upload_to="logos", null=True)
    image = models.TextField(default='ubuntu')
    opened = models.BooleanField(default=False)

    def __str__(self):
        return self.name
