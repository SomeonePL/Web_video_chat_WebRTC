# Generated by Django 3.1.1 on 2020-09-27 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='number',
            field=models.SlugField(blank=True, max_length=8),
        ),
    ]
