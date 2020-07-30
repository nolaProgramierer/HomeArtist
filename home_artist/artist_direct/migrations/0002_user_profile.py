# Generated by Django 3.0.8 on 2020-07-29 23:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artist_direct', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=24)),
                ('l_name', models.CharField(max_length=24)),
                ('bio', models.TextField(blank=True)),
                ('location', models.CharField(choices=[('US', 'United States'), ('CN', 'Canada'), ('EU', 'Europe')], default='US', max_length=2)),
                ('genre', models.CharField(choices=[('Solo', 'Solo'), ('Chamber', 'Chamber'), ('Musical Theater', 'Musical_Theater')], default='Solo', max_length=24)),
                ('instrument', models.CharField(max_length=24)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
