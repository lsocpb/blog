# Generated by Django 5.0.4 on 2024-04-15 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='short_description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]