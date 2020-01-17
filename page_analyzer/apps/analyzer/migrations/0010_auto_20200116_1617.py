# Generated by Django 2.2.7 on 2020-01-16 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0009_auto_20200116_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(blank=True, default='', max_length=15)),
                ('count', models.PositiveSmallIntegerField(null=True)),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='analyzer.Analysis')),
            ],
        ),
        migrations.DeleteModel(
            name='Heading',
        ),
    ]
