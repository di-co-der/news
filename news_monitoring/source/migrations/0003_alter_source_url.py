# Generated by Django 5.0.13 on 2025-04-01 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('source', '0002_source_tagged_companies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='url',
            field=models.URLField(max_length=500),
        ),
    ]
