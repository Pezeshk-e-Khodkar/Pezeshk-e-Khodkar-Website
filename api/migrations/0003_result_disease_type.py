# Generated by Django 4.0.2 on 2023-03-24 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_result_basal_cell_carcinomas_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='disease_type',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
