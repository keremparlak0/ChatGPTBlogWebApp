# Generated by Django 4.0.3 on 2023-04-29 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0005_alter_author_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='pictures'),
        ),
    ]
