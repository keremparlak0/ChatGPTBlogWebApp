# Generated by Django 4.2 on 2023-04-26 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("author", "0003_alter_author_img_alter_library_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="img",
            field=models.ImageField(
                blank=True, null=True, upload_to="library/images", verbose_name="Resim"
            ),
        ),
        migrations.AlterField(
            model_name="blog",
            name="banner",
            field=models.ImageField(upload_to="library/banners"),
        ),
    ]