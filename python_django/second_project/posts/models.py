from django.db import models


# Create your models here.


class Post(models.Model):
    text = models.TextField(verbose_name="текст")

    def __str__(self) -> str:
        return self.text[:50]

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
