# Generated by Django 3.2.16 on 2023-10-23 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_post_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='author',
        ),
    ]