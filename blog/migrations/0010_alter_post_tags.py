# Generated by Django 4.2.11 on 2024-05-29 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_rename_featured_image_post_featured_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, default=None, to='blog.tag'),
        ),
    ]