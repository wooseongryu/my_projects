# Generated by Django 2.2 on 2022-10-22 08:43

import board.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_user_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(error_messages={'unique': '해당 닉네임은 이미 사용중입니다!'}, max_length=15, null=True, unique=True, validators=[board.validators.validate_no_special_charactors]),
        ),
    ]
