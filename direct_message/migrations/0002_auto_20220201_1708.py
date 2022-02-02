# Generated by Django 3.1.4 on 2022-02-01 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20220128_2101'),
        ('direct_message', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_recipient', to='accounts.profile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_sender', to='accounts.profile')),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='on_chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='direct_message.chat'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.RemoveField(
            model_name= 'message',
            name= 'recipient',
        ),
    ]