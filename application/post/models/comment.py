"""
评论模型
"""

from django.db import models


class Comment(models.Model):
    content = models.TextField(max_length=255, verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    refer_post = models.ForeignKey('post.Post', on_delete=models.CASCADE, verbose_name='所属帖子')
    author = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='评论者')

    refer_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='回复对象')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content
