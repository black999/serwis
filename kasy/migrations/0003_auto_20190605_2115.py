# Generated by Django 2.2 on 2019-06-05 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kasy', '0002_auto_20190604_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podatnik',
            name='nip',
            field=models.CharField(max_length=13, unique=True),
        ),
    ]
