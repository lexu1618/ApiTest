# Generated by Django 3.1 on 2021-02-03 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyAPP', '0015_db_project_header'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_step',
            name='public_header',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
