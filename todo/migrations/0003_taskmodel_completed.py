# Generated by Django 2.1 on 2018-08-10 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20180810_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskmodel',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
