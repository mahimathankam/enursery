# Generated by Django 5.0.2 on 2024-05-05 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0004_contact_delete_newproduct'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='name',
            new_name='contact_name',
        ),
    ]
