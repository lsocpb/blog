# Generated by Django 4.2.11 on 2024-04-17 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_post_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='featured_image',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]