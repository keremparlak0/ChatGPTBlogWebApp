# Generated by Django 4.0.3 on 2023-04-29 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0006_alter_author_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='picture',
            field=models.ImageField(blank=True, upload_to='pictures/'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='banner',
            field=models.ImageField(upload_to='banners/'),
        ),
    ]