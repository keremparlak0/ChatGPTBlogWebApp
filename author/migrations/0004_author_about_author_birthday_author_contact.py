# Generated by Django 4.0.3 on 2023-04-29 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0003_rename_text_draft_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='about',
            field=models.CharField(default='', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='contact',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]
