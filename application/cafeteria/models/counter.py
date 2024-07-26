"""
窗口模型
"""

from django.db import models


class Counter(models.Model):
    cafeteria = models.ForeignKey('cafeteria.Cafeteria', on_delete=models.CASCADE, related_name='所属食堂')
    name = models.CharField(max_length=50, verbose_name='窗口名称', unique=True)
    description = models.TextField(max_length=200, verbose_name='窗口描述', blank=True, default='这个窗口很懒，什么都没有留下……')
    image = models.ImageField(upload_to='counter/', default='counter/default.png', verbose_name='窗口图片')
    floor = models.IntegerField(verbose_name='楼层', default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '窗口'
        verbose_name_plural = verbose_name

