# Generated by Django 3.1.4 on 2020-12-23 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20201223_1800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='airtrafficcontroller',
            name='social_links',
        ),
        migrations.AddField(
            model_name='socialmedia',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='social_links', to='users.airtrafficcontroller', verbose_name='User'),
            preserve_default=False,
        ),
    ]