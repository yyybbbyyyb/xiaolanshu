"""
帖子模型
"""

from django.db import models


class Post(models.Model):
    dish = models.ForeignKey('cafeteria.Dish', on_delete=models.CASCADE, related_name='所属菜品')
    title = models.CharField(max_length=50, verbose_name='帖子标题')
    content = models.TextField(max_length=500, verbose_name='帖子内容')
    author = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    images = models.TextField(max_length=1024, verbose_name='图片url集', blank=True)

    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title