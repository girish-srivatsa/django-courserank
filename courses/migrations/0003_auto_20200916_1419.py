# Generated by Django 3.1.1 on 2020-09-16 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20200916_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_instructor',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_code',
            field=models.CharField(max_length=10),
        ),
    ]
