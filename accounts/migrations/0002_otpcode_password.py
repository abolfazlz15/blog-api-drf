# Generated by Django 4.1.1 on 2022-09-16 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='otpcode',
            name='password',
            field=models.CharField(max_length=4, null=True),
        ),
    ]
