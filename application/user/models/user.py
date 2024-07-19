"""
user's info model
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    user's info model
    """
    username = models.CharField(max_length=20, unique=True, verbose_name='用户名', error_messages={'unique': '用户名已存在'},)
    password = models.CharField(max_length=256, verbose_name='密码')
    email = models.EmailField(max_length=255, verbose_name='邮箱', unique=True, error_messages={'unique': '邮箱已存在'})

    student_id = models.CharField(max_length=10, verbose_name='学号', null=True, blank=True, unique=True, error_messages={'unique': '学号已存在'})
    gender_choices = (
        ('null', '沃尔玛购物袋'),
        ('male', '男'),
        ('female', '女')
    )
    gender = models.CharField(choices=gender_choices, max_length=6, default='null', verbose_name='性别')
    intorduction = models.TextField(max_length=200, verbose_name='个人简介', default='这个人很懒，什么都没有留下')
    avatar = models.ImageField(upload_to='media/avatar/', default='media/avatar/default.png', verbose_name='头像')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_login_at = models.DateTimeField(auto_now=True, verbose_name='最后登录时间')

    # collections = models.ManyToManyField('post.Post', related_name='收藏列表', blank=True, verbose_name='收藏', through='Collection')

    isDelete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username