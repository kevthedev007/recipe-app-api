# Generated by Django 3.2.16 on 2022-11-19 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='kelvin', max_length=255),
            preserve_default=False,
        ),
    ]