# Generated by Django 3.2.12 on 2022-03-13 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0002_topic_dt'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='title',
            field=models.CharField(default='無題', max_length=200, verbose_name='タイトル'),
            preserve_default=False,
        ),
    ]
