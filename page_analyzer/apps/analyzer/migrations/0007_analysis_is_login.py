# Generated by Django 2.2.7 on 2020-01-15 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0006_heading_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='is_login',
            field=models.BooleanField(default=False),
        ),
    ]
