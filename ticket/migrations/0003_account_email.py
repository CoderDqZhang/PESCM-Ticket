# Generated by Django 2.1.2 on 2019-01-14 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_auto_20190114_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='邮件地址'),
        ),
    ]