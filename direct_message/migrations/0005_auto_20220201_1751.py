# Generated by Django 3.1.4 on 2022-02-01 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('direct_message', '0004_message_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]