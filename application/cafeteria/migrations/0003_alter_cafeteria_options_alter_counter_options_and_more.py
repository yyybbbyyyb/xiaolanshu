# Generated by Django 4.2.3 on 2024-07-24 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cafeteria', '0002_alter_counter_options_alter_counter_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cafeteria',
            options={'verbose_name': '食堂', 'verbose_name_plural': '食堂'},
        ),
        migrations.AlterModelOptions(
            name='counter',
            options={'verbose_name': '窗口', 'verbose_name_plural': '窗口'},
        ),
        migrations.AlterModelOptions(
            name='dish',
            options={'verbose_name': '菜品', 'verbose_name_plural': '菜品'},
        ),
    ]
