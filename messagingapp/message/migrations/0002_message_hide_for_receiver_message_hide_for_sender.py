# Generated by Django 4.2.4 on 2023-08-10 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='hide_for_receiver',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='hide_for_sender',
            field=models.BooleanField(default=False),
        ),
    ]
