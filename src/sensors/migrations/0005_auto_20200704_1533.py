# Generated by Django 3.0.7 on 2020-07-04 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0004_stargate_temp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stargate',
            old_name='timestamp',
            new_name='created',
        ),
        migrations.AddField(
            model_name='stargate',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='stargate',
            name='name',
            field=models.TextField(default='SG1'),
        ),
        migrations.AlterField(
            model_name='mydata',
            name='debug_mode',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mydata',
            name='nmod_gps_ok',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mydata',
            name='nmod_nav_ok',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mydata',
            name='set_polaris_ok',
            field=models.BooleanField(default=False),
        ),
    ]
