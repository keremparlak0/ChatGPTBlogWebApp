# Generated by Django 4.0.3 on 2023-04-27 13:59

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draft',
            name='text',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
