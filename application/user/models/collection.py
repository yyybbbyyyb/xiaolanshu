# from django.db import models
#
#
# class Collection(models.Model):
#     collector = models.ForeignKey(
#         'User', on_delete=models.CASCADE, null=False, db_index=True,
#         related_name='collectors'
#     )
#     # collections = models.ForeignKey(
#     #     'post.Post', on_delete=models.CASCADE, null=False, db_index=True,
#     #     related_name='collections'
#     # )
#     created_at = models.DateTimeField(blank=False, null=False, auto_now_add=True, verbose_name='创建时间')
#
#     class Meta:
#         ordering = ['-created_at']
#         db_table = 'collection'
#         verbose_name = '收藏'
#         verbose_name_plural = '收藏'
