# Generated by Django 5.2.1 on 2025-05-23 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='liked',
            new_name='liked_by',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='wishlisted',
            new_name='wishlisted_by',
        ),
    ]
