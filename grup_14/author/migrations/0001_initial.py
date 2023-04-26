# Generated by Django 4.2 on 2023-04-26 11:15

import ckeditor.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("taggit", "0005_auto_20220424_2025"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=50, verbose_name="Ad")),
                ("last_name", models.CharField(max_length=50, verbose_name="Soyad")),
                ("email", models.EmailField(max_length=254, verbose_name="E-posta")),
                (
                    "slug",
                    models.SlugField(blank=True, unique=True, verbose_name="Slug"),
                ),
                (
                    "about",
                    models.TextField(
                        blank=True, max_length=250, verbose_name="Hakkında"
                    ),
                ),
                (
                    "contact",
                    models.URLField(blank=True, null=True, verbose_name="İletişim"),
                ),
                (
                    "birthday",
                    models.DateField(
                        blank=True, null=True, verbose_name="Doğum Tarihi"
                    ),
                ),
                (
                    "img",
                    models.ImageField(
                        blank=True, null=True, upload_to="img", verbose_name="Resim"
                    ),
                ),
                (
                    "join_date",
                    models.DateField(
                        default=datetime.date.today, verbose_name="Katılım Tarihi"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name": "Yazar", "verbose_name_plural": "Yazarlar",},
        ),
        migrations.CreateModel(
            name="Library",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="img")),
            ],
        ),
        migrations.CreateModel(
            name="Draft",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                ("text", ckeditor.fields.RichTextField(blank=True, null=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="author.author"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                ("slug", models.SlugField(blank=True, default="", unique=True)),
                ("description", models.TextField(max_length=200)),
                ("date", models.DateField(auto_now=True)),
                ("banner", models.ImageField(upload_to="banners")),
                ("likes", models.PositiveIntegerField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="author.author"
                    ),
                ),
                (
                    "draft",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="author.draft"
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Tags",
                    ),
                ),
            ],
        ),
    ]
