# Generated by Django 3.0.1 on 2021-03-28 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0036_student_school_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='number',
            field=models.CharField(default='', max_length=15),
        ),
    ]
