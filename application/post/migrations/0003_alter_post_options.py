# Generated by Django 4.2.3 on 2024-07-24 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_alter_post_images'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': '帖子', 'verbose_name_plural': '帖子'},
        ),
    ]
