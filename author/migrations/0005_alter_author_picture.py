# Generated by Django 4.0.3 on 2023-04-29 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0004_author_about_author_birthday_author_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='picture',
            field=models.ImageField(blank=True, default='', null=True, upload_to='pictures'),
        ),
    ]