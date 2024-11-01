# Generated by Django 4.2.3 on 2024-07-24 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_alter_post_images'),
        ('user', '0004_postcollection_eatcollection_countercollection_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cafeteriacollection',
            old_name='collections',
            new_name='cafeteria',
        ),
        migrations.RenameField(
            model_name='countercollection',
            old_name='collections',
            new_name='counter',
        ),
        migrations.RenameField(
            model_name='eatcollection',
            old_name='collections',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='postcollection',
            old_name='collections',
            new_name='post',
        ),
        migrations.AlterField(
            model_name='user',
            name='eat_collections',
            field=models.ManyToManyField(blank=True, related_name='eaten_by', through='user.EatCollection', to='post.post'),
        ),
        migrations.AlterField(
            model_name='user',
            name='post_collections',
            field=models.ManyToManyField(blank=True, related_name='collected_by', through='user.PostCollection', to='post.post'),
        ),
    ]
