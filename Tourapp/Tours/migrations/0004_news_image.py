# Generated by Django 4.0.4 on 2022-05-04 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tours', '0003_tour_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.ImageField(null=True, upload_to='news/%Y/%m'),
        ),
    ]