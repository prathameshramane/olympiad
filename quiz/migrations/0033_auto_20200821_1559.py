# Generated by Django 3.0.1 on 2020-08-21 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0032_remove_quiz_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='img1',
            field=models.ImageField(blank=True, null=True, upload_to='option1/', verbose_name='Image1'),
        ),
        migrations.AlterField(
            model_name='question',
            name='img2',
            field=models.ImageField(blank=True, null=True, upload_to='option2/', verbose_name='Image2'),
        ),
        migrations.AlterField(
            model_name='question',
            name='img3',
            field=models.ImageField(blank=True, null=True, upload_to='option3/', verbose_name='Image3'),
        ),
        migrations.AlterField(
            model_name='question',
            name='img4',
            field=models.ImageField(blank=True, null=True, upload_to='option4/', verbose_name='Image4'),
        ),
    ]
