# Generated by Django 3.2.8 on 2021-10-31 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_data', '0004_auto_20211030_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='apistoremodel',
            name='sync_url',
            field=models.CharField(blank=True, max_length=550, null=True),
        ),
    ]
