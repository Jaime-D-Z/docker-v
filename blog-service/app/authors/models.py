from django.db import models


class Author(models.Model):
    display_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ['display_name']

    def __str__(self):
        return self.display_name

