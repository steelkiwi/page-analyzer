# Generated by Django 2.2 on 2019-10-03 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactusrequest',
            options={'ordering': ['id'], 'verbose_name': 'Contact Us Request', 'verbose_name_plural': 'Contact Us Requests'},
        ),
        migrations.AlterModelOptions(
            name='supportcentercategory',
            options={'ordering': ['slug'], 'verbose_name': 'Support Center', 'verbose_name_plural': 'Support Center'},
        ),
        migrations.AlterModelOptions(
            name='supportcenterelement',
            options={'ordering': ('category', 'order'), 'verbose_name': 'Support Center Element', 'verbose_name_plural': 'Support Center Elements'},
        ),
    ]