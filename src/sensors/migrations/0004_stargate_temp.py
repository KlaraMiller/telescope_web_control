# Generated by Django 3.0.7 on 2020-07-04 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0003_mydata_stargate'),
    ]

    operations = [
        migrations.AddField(
            model_name='stargate',
            name='temp',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
