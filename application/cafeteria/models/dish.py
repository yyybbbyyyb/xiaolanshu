"""
菜品模型
"""

from django.db import models


class Dish(models.Model):
    counter = models.ForeignKey('cafeteria.Counter', on_delete=models.CASCADE, related_name='所属窗口')
    name = models.CharField(max_length=50, verbose_name='菜品名称')
    description = models.TextField(max_length=200, verbose_name='菜品描述', blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='菜品价格')
    image = models.ImageField(upload_to='dish/', default='dish/default.png', verbose_name='菜品图片')
