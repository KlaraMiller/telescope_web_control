# Generated by Django 3.0.7 on 2020-07-04 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0005_auto_20200704_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stargate',
            name='temp',
        ),
        migrations.AlterField(
            model_name='stargate',
            name='name',
            field=models.CharField(default='SG1', max_length=10),
        ),
    ]
