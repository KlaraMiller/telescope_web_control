# Generated by Django 3.0.7 on 2020-07-04 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sg1',
            name='gps_data',
            field=models.TextField(default='-'),
            preserve_default=False,
        ),
    ]
