# Generated by Django 5.0.7 on 2024-07-21 10:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cafeteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='食堂名称')),
                ('description', models.TextField(blank=True, max_length=200, verbose_name='食堂描述')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='食堂地址')),
                ('image', models.ImageField(default='cafeteria/default.png', upload_to='cafeteria/', verbose_name='食堂图片')),
            ],
        ),
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='窗口名称')),
                ('description', models.TextField(blank=True, max_length=200, verbose_name='窗口描述')),
                ('image', models.ImageField(default='counter/default.png', upload_to='counter/', verbose_name='窗口图片')),
                ('floor', models.IntegerField(default=1, verbose_name='楼层')),
                ('cafeteria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='所属食堂', to='cafeteria.cafeteria')),
            ],
            options={
                'verbose_name': '窗口',
                'verbose_name_plural': '窗口',
                'db_table': 'counter',
                'ordering': ['floor'],
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='菜品名称')),
                ('description', models.TextField(blank=True, max_length=200, verbose_name='菜品描述')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='菜品价格')),
                ('image', models.ImageField(default='dish/default.png', upload_to='dish/', verbose_name='菜品图片')),
                ('counter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='所属窗口', to='cafeteria.counter')),
            ],
        ),
    ]
