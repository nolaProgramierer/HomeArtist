# Generated by Django 3.0.8 on 2020-08-04 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist_direct', '0009_comment_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(blank=True),
        ),
    ]
