# Generated by Django 4.1.1 on 2023-02-22 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='full name'),
        ),
    ]