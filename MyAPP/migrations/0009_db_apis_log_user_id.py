# Generated by Django 3.1.5 on 2021-01-29 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyAPP', '0008_db_apis_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_apis_log',
            name='user_id',
            field=models.CharField(max_length=10, null=True),
        ),
    ]