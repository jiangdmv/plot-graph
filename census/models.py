from django.db import models

filetypeChoices = (('\t', 'txt'), (',', 'csv'))


# Create your models here.
class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    filetype = models.CharField(max_length=6, choices=filetypeChoices, default="tab")
    target = models.CharField(max_length=150, verbose_name="Enter a target column")
    alpha = models.FloatField(max_length=150, verbose_name="Enter an alpha level", default=0.05)

    def delete(self, *args, **kwargs):
        self.document.delete()
        super().delete(*args, **kwargs)
