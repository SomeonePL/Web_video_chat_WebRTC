# Generated by Django 3.1.1 on 2020-09-30 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0005_validroom_validation_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='validroom',
            name='validation_username',
            field=models.SlugField(blank=True, max_length=8),
        ),
    ]
