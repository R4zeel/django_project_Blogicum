# Generated by Django 3.2.16 on 2023-10-23 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_rename_user_comment_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='text',
        ),
    ]