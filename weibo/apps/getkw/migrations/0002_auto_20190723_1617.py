# Generated by Django 2.2.3 on 2019-07-23 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getkw', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kerword',
            name='id',
        ),
        migrations.AddField(
            model_name='kerword',
            name='object_id',
            field=models.CharField(default='', max_length=50, primary_key=True, serialize=False, verbose_name='主键'),
        ),
    ]
