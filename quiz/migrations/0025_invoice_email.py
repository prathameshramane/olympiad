# Generated by Django 3.0.1 on 2020-08-04 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0024_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
