# Generated by Django 4.1.1 on 2023-02-23 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_full_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OTPCode',
        ),
    ]