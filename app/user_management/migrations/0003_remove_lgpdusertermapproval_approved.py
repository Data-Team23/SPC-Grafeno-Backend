# Generated by Django 4.2.16 on 2024-10-31 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_rename_term_type_lgpdgeneralterm_term_itens_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lgpdusertermapproval',
            name='approved',
        ),
    ]