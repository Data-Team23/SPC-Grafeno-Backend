# Generated by Django 3.1.3 on 2024-10-20 22:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_auto_20241020_2228'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='_id',
            new_name='user_id',
        ),
    ]