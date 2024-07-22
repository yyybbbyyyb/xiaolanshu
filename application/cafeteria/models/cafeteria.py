"""
食堂模型
"""

from django.db import models


class Cafeteria(models.Model):
    name = models.CharField(max_length=50, verbose_name='食堂名称', unique=True)
    description = models.TextField(max_length=200, verbose_name='食堂描述', blank=True)
    address = models.CharField(max_length=255, verbose_name='食堂地址', blank=True)
    image = models.ImageField(upload_to='cafeteria/', default='cafeteria/default.png', verbose_name='食堂图片')

    def __str__(self):
        return self.name

