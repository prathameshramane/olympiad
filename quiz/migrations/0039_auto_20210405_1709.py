# Generated by Django 3.0.1 on 2021-04-05 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0038_auto_20210405_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school_register',
            name='contact',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='school_register',
            name='pmobile',
            field=models.CharField(max_length=15),
        ),
    ]
