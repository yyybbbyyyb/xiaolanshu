"""
user's info models
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    user's info models
    AbstractUser:
        内置了date_joined字段，用于记录用户注册时间
        内置了last_login字段，用于记录用户最后登录时间
        内置了is_active字段，用于记录用户是否激活
        内置了is_staff字段，用于记录用户是否是员工
        内置了is_superuser字段，用于记录用户是否是超级用户
    """
    username = models.CharField(max_length=20, unique=True, verbose_name='用户名', error_messages={'unique': '用户名已存在'},)
    password = models.CharField(max_length=256, verbose_name='密码')
    email = models.EmailField(max_length=255, verbose_name='邮箱', unique=True, error_messages={'unique': '邮箱已存在'})

    student_id = models.CharField(max_length=10, verbose_name='学号', null=True, blank=True, unique=True,
                                  error_messages={'unique': '学号已存在'})
    gender_choices = (
        ('null', '沃尔玛购物袋'),
        ('male', '男'),
        ('female', '女')
    )
    gender = models.CharField(choices=gender_choices, max_length=6, default='null', verbose_name='性别')
    introduction = models.TextField(max_length=200, verbose_name='个人简介', default='这个人很懒，什么都没有留下')
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default.png', verbose_name='头像')

    cafeteria_collections = models.ManyToManyField('cafeteria.Cafeteria', related_name='收藏食堂列表', blank=True,
                                                   through='CafeteriaCollection')
    counter_collections = models.ManyToManyField('cafeteria.Counter', related_name='收藏窗口列表', blank=True,
                                                 through='CounterCollection')
    post_collections = models.ManyToManyField('post.Post', related_name='collected_by', blank=True,
                                              through='PostCollection')
    eat_collections = models.ManyToManyField('post.Post', related_name='eaten_by', blank=True,
                                             through='EatCollection')

    isDelete = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    class Meta:
        ordering = ['-date_joined']
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username
