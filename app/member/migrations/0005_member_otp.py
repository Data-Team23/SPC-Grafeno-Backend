# Generated by Django 3.1.3 on 2024-10-20 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_auto_20241020_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
