# Generated by Django 2.2.6 on 2019-10-10 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_made_email_field_unique_and_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='is verified by admin'),
        ),
    ]
