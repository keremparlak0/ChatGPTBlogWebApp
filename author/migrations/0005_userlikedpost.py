# Generated by Django 4.2.1 on 2023-05-30 21:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('author', '0004_blog_search_post_blog_stemmed_author_name_surname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLikedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_by', to='author.blog')),
                ('tags', models.ManyToManyField(to='taggit.tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
