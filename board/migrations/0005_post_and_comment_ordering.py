# Generated by Django 2.2 on 2022-10-28 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_like'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-dt_created']},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-dt_created']},
        ),
    ]
