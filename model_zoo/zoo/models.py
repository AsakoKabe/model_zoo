from django.db import models


class ModelCV(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    url = models.CharField(max_length=16)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Модель"
        verbose_name_plural = "Модели"
        ordering = ['-created_at']


class RequestCV(models.Model):
    input_img = models.ImageField(upload_to="images/%Y/%m/%d/")
    output_img = models.ImageField(upload_to="images/%Y/%m/%d/", default=None)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    model = models.ForeignKey(ModelCV, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Запрос"
        verbose_name_plural = "Запросы"
        ordering = ['-created_at']
